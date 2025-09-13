#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

interface ExportInfo {
  name: string;
  isDefault: boolean;
  isNamed: boolean;
  originalLine: string;
}

class IndexGenerator {
  private readonly supportedExtensions = ['.ts', '.tsx', '.js', '.jsx'];
  private readonly excludePatterns = [
    /\.test\./,
    /\.spec\./,
    /\.d\.ts$/,
    /index\./,
    /\.stories\./,
    /\.config\./
  ];

  /**
   * Main entry point - generates index.ts files recursively
   */
  async generateIndexFiles(rootDir: string, options: { recursive?: boolean; dryRun?: boolean } = {}): Promise<void> {
    const { recursive = true, dryRun = false } = options;
    
    console.log(`🚀 Starting index.ts generation for: ${rootDir}`);
    console.log(`📋 Options: recursive=${recursive}, dryRun=${dryRun}`);

    if (!fs.existsSync(rootDir)) {
      throw new Error(`Directory does not exist: ${rootDir}`);
    }

    await this.processDirectory(rootDir, recursive, dryRun);
    console.log(`✅ Index generation complete!`);
  }

  /**
   * Process a single directory
   */
  private async processDirectory(dirPath: string, recursive: boolean, dryRun: boolean): Promise<void> {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });
    const files: string[] = [];
    const subdirs: string[] = [];

    // Separate files and subdirectories
    for (const entry of entries) {
      if (entry.isFile() && this.isValidFile(entry.name)) {
        files.push(entry.name);
      } else if (entry.isDirectory() && !entry.name.startsWith('.')) {
        subdirs.push(entry.name);
      }
    }

    // Generate index.ts for current directory if it has valid files
    if (files.length > 0) {
      await this.generateIndexForDirectory(dirPath, files, dryRun);
    }

    // Recursively process subdirectories
    if (recursive) {
      for (const subdir of subdirs) {
        const subdirPath = path.join(dirPath, subdir);
        await this.processDirectory(subdirPath, recursive, dryRun);
      }
    }
  }

  /**
   * Generate index.ts file for a specific directory
   */
  private async generateIndexForDirectory(dirPath: string, files: string[], dryRun: boolean): Promise<void> {
    const exports: string[] = [];
    const reexports: string[] = [];

    console.log(`\n📁 Processing directory: ${dirPath}`);

    for (const file of files) {
      const filePath = path.join(dirPath, file);
      const exportInfo = await this.analyzeFileExports(filePath);
      
      if (exportInfo.length === 0) {
        console.log(`   ⚠️  No exports found in ${file}`);
        continue;
      }

      const fileWithoutExt = this.removeExtension(file);
      const statements = this.generateExportStatements(exportInfo, fileWithoutExt);
      
      exports.push(...statements.exports);
      reexports.push(...statements.reexports);

      console.log(`   ✨ ${file}: ${exportInfo.length} export(s) found`);
    }

    if (exports.length === 0 && reexports.length === 0) {
      console.log(`   ⚠️  No valid exports found, skipping index.ts generation`);
      return;
    }

    const indexContent = this.generateIndexContent(exports, reexports);
    const indexPath = path.join(dirPath, 'index.ts');

    if (dryRun) {
      console.log(`   📄 Would generate ${indexPath}:`);
      console.log(indexContent.split('\n').map(line => `      ${line}`).join('\n'));
    } else {
      fs.writeFileSync(indexPath, indexContent, 'utf8');
      console.log(`   ✅ Generated ${indexPath}`);
    }
  }

  /**
   * Analyze a file to extract export information
   */
  private async analyzeFileExports(filePath: string): Promise<ExportInfo[]> {
    const content = fs.readFileSync(filePath, 'utf8');
    const exports: ExportInfo[] = [];

    // Split content into lines for analysis
    const lines = content.split('\n');

    for (const line of lines) {
      const trimmedLine = line.trim();
      
      // Skip comments and empty lines
      if (trimmedLine.startsWith('//') || trimmedLine.startsWith('/*') || !trimmedLine) {
        continue;
      }

      // Match export patterns
      const exportPatterns = [
        // export default class/function/const Name
        /^export\s+default\s+(?:class|function|const|let|var|interface|type|enum)\s+(\w+)/,
        // export default Name
        /^export\s+default\s+(\w+)/,
        // export { name1, name2 }
        /^export\s+\{\s*([^}]+)\s*\}/,
        // export const/let/var name
        /^export\s+(?:const|let|var)\s+(\w+)/,
        // export function name
        /^export\s+function\s+(\w+)/,
        // export class name
        /^export\s+class\s+(\w+)/,
        // export interface name
        /^export\s+interface\s+(\w+)/,
        // export type name
        /^export\s+type\s+(\w+)/,
        // export enum name
        /^export\s+enum\s+(\w+)/,
      ];

      for (const pattern of exportPatterns) {
        const match = trimmedLine.match(pattern);
        if (match) {
          if (trimmedLine.includes('default')) {
            exports.push({
              name: match[1],
              isDefault: true,
              isNamed: false,
              originalLine: trimmedLine
            });
          } else if (trimmedLine.startsWith('export {')) {
            // Handle destructured exports
            const names = match[1].split(',').map(name => name.trim());
            for (const name of names) {
              const cleanName = name.replace(/\s+as\s+\w+/, ''); // Remove 'as alias'
              exports.push({
                name: cleanName,
                isDefault: false,
                isNamed: true,
                originalLine: trimmedLine
              });
            }
          } else {
            exports.push({
              name: match[1],
              isDefault: false,
              isNamed: true,
              originalLine: trimmedLine
            });
          }
          break;
        }
      }
    }

    return exports;
  }

  /**
   * Generate modern export statements
   */
  private generateExportStatements(exportInfo: ExportInfo[], fileName: string): { exports: string[]; reexports: string[] } {
    const exports: string[] = [];
    const reexports: string[] = [];

    const defaultExports = exportInfo.filter(e => e.isDefault);
    const namedExports = exportInfo.filter(e => e.isNamed);

    // Handle default exports - re-export as named
    for (const defaultExport of defaultExports) {
      reexports.push(`export { default as ${defaultExport.name} } from './${fileName}';`);
    }

    // Handle named exports - re-export directly
    if (namedExports.length > 0) {
      const namedExportNames = namedExports.map(e => e.name).join(', ');
      reexports.push(`export { ${namedExportNames} } from './${fileName}';`);
    }

    return { exports, reexports };
  }

  /**
   * Generate the final index.ts content
   */
  private generateIndexContent(exports: string[], reexports: string[]): string {
    const lines: string[] = [];
    
    // Add file header
    lines.push('// Auto-generated index file');
    lines.push('// Run `npm run generate:index` to regenerate');
    lines.push('');

    // Add re-exports (modern approach)
    if (reexports.length > 0) {
      lines.push(...reexports);
    }

    // Add direct exports if any
    if (exports.length > 0) {
      lines.push('');
      lines.push(...exports);
    }

    lines.push(''); // Final newline

    return lines.join('\n');
  }

  /**
   * Check if file should be processed
   */
  private isValidFile(filename: string): boolean {
    const ext = path.extname(filename);
    
    // Check extension
    if (!this.supportedExtensions.includes(ext)) {
      return false;
    }

    // Check exclude patterns
    for (const pattern of this.excludePatterns) {
      if (pattern.test(filename)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Remove file extension
   */
  private removeExtension(filename: string): string {
    return filename.replace(/\.[^/.]+$/, '');
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const generator = new IndexGenerator();

  if (args.length === 0) {
    console.log(`
Usage: ts-node index-generator.ts <directory> [options]

Options:
  --no-recursive    Don't process subdirectories
  --dry-run        Show what would be generated without writing files

Examples:
  ts-node index-generator.ts ./src/components
  ts-node index-generator.ts ./src --dry-run
  ts-node index-generator.ts ./src/hooks --no-recursive
`);
    process.exit(1);
  }

  const directory = args[0];
  const options = {
    recursive: !args.includes('--no-recursive'),
    dryRun: args.includes('--dry-run')
  };

  generator.generateIndexFiles(directory, options).catch(error => {
    console.error('❌ Error:', error.message);
    process.exit(1);
  });
}

module.exports = { IndexGenerator };