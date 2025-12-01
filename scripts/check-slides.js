#!/usr/bin/env node

/**
 * Marp スライド検証スクリプト（汎用版）
 *
 * 使い方:
 *   node scripts/check-slides.js overflow <file-or-dir>   # オーバーフロー検出
 *   node scripts/check-slides.js links <dist-dir>          # リンク切れ検出
 *
 * 例:
 *   node scripts/check-slides.js overflow src/01-intro.md
 *   node scripts/check-slides.js overflow src/
 *   node scripts/check-slides.js links dist/
 *
 * 対応ブラウザ（自動検出）:
 *   - Google Chrome
 *   - Chromium
 *   - Microsoft Edge
 *   - Playwright Chromium (bunx playwright install chromium でインストール)
 */

const fs = require('fs');
const fsp = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// ANSI カラーコード
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * インストール済みのChromiumベースのブラウザを検出
 */
function detectInstalledBrowser() {
  const browserPaths = [
    // Linux
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    '/opt/google/chrome/chrome',
    '/usr/bin/microsoft-edge',
    '/usr/bin/microsoft-edge-stable',
    '/snap/bin/chromium',
    // macOS
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  ];

  for (const browserPath of browserPaths) {
    if (fs.existsSync(browserPath)) {
      return { path: browserPath, name: path.basename(browserPath) };
    }
  }

  // which コマンドで検索
  const commands = ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'microsoft-edge'];
  for (const cmd of commands) {
    try {
      const result = execSync(`which ${cmd} 2>/dev/null`, { encoding: 'utf-8' }).trim();
      if (result) return { path: result, name: cmd };
    } catch (err) {}
  }

  // Playwright の Chromium を検索
  const homeDir = os.homedir();
  const playwrightCacheDirs = [
    path.join(homeDir, '.cache', 'ms-playwright'),
    path.join(homeDir, 'Library', 'Caches', 'ms-playwright'),
  ];

  for (const cacheDir of playwrightCacheDirs) {
    if (fs.existsSync(cacheDir)) {
      try {
        const entries = fs.readdirSync(cacheDir);
        const chromiumDir = entries.find(e => e.startsWith('chromium-'));
        if (chromiumDir) {
          const chromiumPaths = [
            path.join(cacheDir, chromiumDir, 'chrome-linux', 'chrome'),
            path.join(cacheDir, chromiumDir, 'chrome-mac', 'Chromium.app', 'Contents', 'MacOS', 'Chromium'),
          ];
          for (const p of chromiumPaths) {
            if (fs.existsSync(p)) {
              return { path: p, name: 'Playwright Chromium' };
            }
          }
        }
      } catch (err) {}
    }
  }

  return null;
}

/**
 * Puppeteer-core を動的にロード、なければインストール
 */
async function loadPuppeteer() {
  try {
    return require('puppeteer-core');
  } catch (err) {
    log('puppeteer-core が見つかりません。インストールします...', 'yellow');
    try {
      execSync('npm install --no-save puppeteer-core', { stdio: 'inherit' });
      return require('puppeteer-core');
    } catch (installErr) {
      log('❌ puppeteer-core のインストールに失敗しました', 'red');
      log('手動でインストールしてください: npm install puppeteer-core', 'yellow');
      process.exit(1);
    }
  }
}

/**
 * Marp CLI コマンドを検出
 */
function detectMarpCommand() {
  // npx を使用（最も汎用的）
  return 'npx --yes @marp-team/marp-cli';
}

/**
 * 単一ファイルのオーバーフローをチェック
 */
async function checkOverflowSingle(markdownPath, browser) {
  const tmpDir = await fsp.mkdtemp(path.join(os.tmpdir(), 'marp-check-'));
  const tmpHtmlPath = path.join(tmpDir, 'output.html');

  try {
    const absoluteMarkdownPath = path.resolve(markdownPath);
    const marpCommand = detectMarpCommand();

    // Marp CLI でビルド
    try {
      execSync(
        `${marpCommand} --no-stdin --html --allow-local-files "${absoluteMarkdownPath}" -o "${tmpHtmlPath}"`,
        { stdio: 'pipe', encoding: 'utf-8' }
      );
    } catch (buildError) {
      log(`❌ ビルドエラー: ${markdownPath}`, 'red');
      return { file: markdownPath, error: buildError.message, overflows: [] };
    }

    const htmlContent = await fsp.readFile(tmpHtmlPath, 'utf-8');

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.setContent(htmlContent, { waitUntil: 'networkidle0' });

    const results = await page.evaluate(() => {
      const sections = Array.from(document.querySelectorAll('section'));
      return sections.map((section, index) => {
        const scrollHeight = section.scrollHeight;
        const clientHeight = section.clientHeight;
        const scrollWidth = section.scrollWidth;
        const clientWidth = section.clientWidth;
        const dataClass = section.getAttribute('data-class') || '';
        const hasVerticalOverflow = scrollHeight > clientHeight;
        const hasHorizontalOverflow = scrollWidth > clientWidth;
        const textContent = section.textContent.trim().substring(0, 50).replace(/\n/g, ' ');

        return {
          slideNumber: index + 1,
          hasOverflow: hasVerticalOverflow || hasHorizontalOverflow,
          hasVerticalOverflow,
          hasHorizontalOverflow,
          overflowHeight: scrollHeight - clientHeight,
          overflowWidth: scrollWidth - clientWidth,
          preview: textContent,
          dataClass
        };
      });
    });

    await page.close();

    const overflows = results.filter(r => r.hasOverflow);
    return {
      file: markdownPath,
      totalSlides: results.length,
      overflows
    };

  } finally {
    try {
      await fsp.rm(tmpDir, { recursive: true, force: true });
    } catch (err) {}
  }
}

/**
 * オーバーフローチェック（ファイルまたはディレクトリ）
 */
async function checkOverflow(targetPath) {
  log(`${colors.bold}Marp Overflow Checker${colors.reset}\n`, 'cyan');

  const stat = await fsp.stat(targetPath);
  let files = [];

  if (stat.isDirectory()) {
    const entries = await fsp.readdir(targetPath);
    files = entries
      .filter(f => f.endsWith('.md') && !f.startsWith('CLAUDE') && !f.startsWith('README'))
      .map(f => path.join(targetPath, f));
  } else {
    files = [targetPath];
  }

  if (files.length === 0) {
    log('対象ファイルがありません', 'yellow');
    return;
  }

  const browserInfo = detectInstalledBrowser();
  if (!browserInfo) {
    log('❌ 対応ブラウザが見つかりません', 'red');
    log('以下のいずれかをインストールしてください:', 'yellow');
    log('  - Google Chrome', 'yellow');
    log('  - Chromium', 'yellow');
    log('  - Microsoft Edge', 'yellow');
    log('  - bunx playwright install chromium', 'yellow');
    process.exit(1);
  }

  log(`✓ ブラウザ: ${browserInfo.name}`, 'green');
  log(`  パス: ${browserInfo.path}\n`, 'cyan');

  const puppeteer = await loadPuppeteer();
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: browserInfo.path,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    let totalSlides = 0;
    let totalOverflows = 0;
    const allResults = [];

    for (const file of files) {
      log(`📄 ${path.basename(file)}`, 'blue');
      const result = await checkOverflowSingle(file, browser);
      allResults.push(result);

      if (result.error) {
        log(`   エラー: ${result.error}`, 'red');
        continue;
      }

      totalSlides += result.totalSlides;
      totalOverflows += result.overflows.length;

      if (result.overflows.length > 0) {
        for (const o of result.overflows) {
          log(`   ❌ スライド ${o.slideNumber}: ${o.overflowHeight}px オーバー`, 'red');
          if (o.dataClass) {
            log(`      クラス: ${o.dataClass}`, 'cyan');
          }
        }
      } else {
        log(`   ✅ すべてOK (${result.totalSlides}スライド)`, 'green');
      }
      console.log('');
    }

    // サマリー
    log(`${'='.repeat(50)}`, 'bold');
    log(`📊 サマリー`, 'bold');
    log(`${'='.repeat(50)}`, 'bold');
    log(`ファイル数: ${files.length}`);
    log(`総スライド数: ${totalSlides}`);
    log(`OK: ${totalSlides - totalOverflows}`, 'green');
    log(`オーバーフロー: ${totalOverflows}`, totalOverflows > 0 ? 'red' : 'green');

    if (totalOverflows > 0) {
      log(`\n💡 推奨対応:`, 'cyan');
      log(`  1. <!-- _class: font-small --> を追加`, 'cyan');
      log(`  2. コンテンツを削減`, 'cyan');
      log(`  3. スライドを分割`, 'cyan');
      process.exit(1);
    } else {
      log(`\n✨ すべてのスライドが正常です！`, 'green');
    }

  } finally {
    await browser.close();
  }
}

/**
 * リンク切れチェック
 */
async function checkLinks(distDir) {
  log(`${colors.bold}Link Checker${colors.reset}\n`, 'cyan');

  const indexPath = path.join(distDir, 'index.html');
  if (!fs.existsSync(indexPath)) {
    log(`❌ ${indexPath} が見つかりません`, 'red');
    process.exit(1);
  }

  const htmlContent = await fsp.readFile(indexPath, 'utf-8');
  const linkPattern = /href="([^"]+\.html)"/g;
  const links = [];
  let match;

  while ((match = linkPattern.exec(htmlContent)) !== null) {
    links.push(match[1]);
  }

  log(`📄 ${links.length} 件のリンクを発見\n`, 'blue');

  let broken = 0;
  for (const link of links) {
    const linkPath = path.join(distDir, link);
    if (fs.existsSync(linkPath)) {
      log(`✅ ${link}`, 'green');
    } else {
      log(`❌ ${link} (存在しません)`, 'red');
      broken++;
    }
  }

  console.log('');
  if (broken > 0) {
    log(`⚠️  ${broken} 件のリンク切れがあります`, 'red');
    process.exit(1);
  } else {
    log(`✨ すべてのリンクが有効です`, 'green');
  }
}

// メイン処理
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.log(`使い方:
  node scripts/check-slides.js overflow <file-or-dir>   # オーバーフロー検出
  node scripts/check-slides.js links <dist-dir>          # リンク切れ検出

例:
  node scripts/check-slides.js overflow src/01-intro.md
  node scripts/check-slides.js overflow src/
  node scripts/check-slides.js links dist/

対応ブラウザ（自動検出）:
  - Google Chrome
  - Chromium
  - Microsoft Edge
  - Playwright Chromium (bunx playwright install chromium)`);
    process.exit(1);
  }

  const command = args[0];
  const target = args[1];

  if (!fs.existsSync(target)) {
    log(`❌ パスが見つかりません: ${target}`, 'red');
    process.exit(1);
  }

  switch (command) {
    case 'overflow':
      await checkOverflow(target);
      break;
    case 'links':
      await checkLinks(target);
      break;
    default:
      log(`❌ 不明なコマンド: ${command}`, 'red');
      process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
