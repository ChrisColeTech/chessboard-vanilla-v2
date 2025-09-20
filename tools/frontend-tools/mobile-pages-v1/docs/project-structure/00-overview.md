# Project Structure Documentation Overview

This folder contains documentation to demystify the mobile-pages-v2 codebase and reduce complexity through understanding the actual implementation, rather than taking shortcuts or making assumptions.

## Purpose
- **Understand before modifying**: Read and comprehend the existing codebase thoroughly
- **Reduce complexity through knowledge**: Map out how components interact 
- **Avoid shortcuts**: Proper analysis prevents introducing bugs or breaking existing functionality
- **Document patterns**: Capture the architectural decisions and design patterns in use

## What I'm Struggling With

### Core Questions I Need Answered:

**Template System Confusion:**
- How exactly does the DependencyManager decide which static templates to copy?
- What's the difference between `ensure_all_dependencies()` and `ensure_static_components()`?
- When do static templates get copied vs when do they get skipped?
- Why does `ensure_static_components()` check `if not output_path.exists()` - is this preventing overwrites?

**Execution Order Mystery:**
- What is the EXACT order of operations during page creation?
- When does dependency scanning happen vs dependency creation?
- Where in the flow do static templates actually get written to disk?
- How does the `regenerate_index_files()` call fit into this?

**Integration Points I Don't Understand:**
- How does the navigation generation integration actually get called?
- Is `_register_parent_and_update_navigation()` actually executing?
- What happens if navigation generation fails - is it caught silently?
- Why do the debug messages show navigation generation working but files don't update?

**Error Handling Gaps:**
- Where are exceptions being caught and hidden?
- How do I know if navigation generation is actually running vs failing silently?
- What's the difference between validation failures vs generation failures?

**Template Engine Behavior:**
- How does the TemplateEngine handle static vs dynamic templates differently?
- What variables are available during static template rendering?
- Does template rendering happen once or multiple times during generation?

### What These Docs Should Answer:

1. **Complete execution trace** of parent page creation from start to finish
2. **Exact file system operations** - when files are created, copied, or overwritten
3. **Integration failure points** - where navigation generation could fail and why
4. **Template resolution logic** - how the system decides which templates to use
5. **Error propagation paths** - how failures bubble up or get swallowed

## Methodology

1. **Read First**: Examine actual code before making changes
2. **Map Interactions**: Understand how components communicate
3. **Trace Execution**: Follow the actual execution path
4. **Document Findings**: Capture understanding for future reference
5. **Verify Understanding**: Test assumptions against actual behavior

## Current Focus

Understanding why navigation generation integration is failing by:
- Mapping the complete page generation workflow
- Identifying all integration points
- Tracing actual execution paths
- Documenting error handling patterns