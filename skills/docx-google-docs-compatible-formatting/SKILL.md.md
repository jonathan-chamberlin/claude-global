---
name: docx-google-docs-compatible-formatting
description: "MUST reference this skill whenever creating, editing, or interacting with .docx files. Contains critical formatting rules that prevent layout breakage when .docx files are opened in Google Docs. Triggers: any .docx creation or editing task, any mention of Word documents, resumes, reports, or professional documents that may be opened in Google Docs."
---

# Google Docs Compatible DOCX Formatting

## Core Problem

Google Docs strips custom tab stops from .docx files. Any layout relying on tab stops (e.g., left-aligned title with right-aligned date on the same line) will collapse into a single run of text with no spacing.

## Rule: Use Invisible Tables Instead of Tab Stops

Never use tab stops for left/right alignment in .docx files. Instead, use borderless two-column tables.

### Pattern: Two-Column Alignment Row

```javascript
const { Table, TableRow, TableCell, Paragraph, TextRun, AlignmentType, BorderStyle, WidthType, VerticalAlign } = require("docx");

const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function twoColRow(leftChildren, rightChildren, contentWidth) {
  const leftWidth = Math.floor(contentWidth * 0.7);
  const rightWidth = contentWidth - leftWidth;
  return new Table({
    width: { size: contentWidth, type: WidthType.DXA },
    columnWidths: [leftWidth, rightWidth],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: noBorders,
            width: { size: leftWidth, type: WidthType.DXA },
            verticalAlign: VerticalAlign.BOTTOM,
            children: [
              new Paragraph({ spacing: { before: 0, after: 0 }, children: leftChildren }),
            ],
          }),
          new TableCell({
            borders: noBorders,
            width: { size: rightWidth, type: WidthType.DXA },
            verticalAlign: VerticalAlign.BOTTOM,
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                spacing: { before: 0, after: 0 },
                children: rightChildren,
              }),
            ],
          }),
        ],
      }),
    ],
  });
}
```

### Usage Example (Resume-Style Row)

```javascript
// contentWidth = pageWidth - leftMargin - rightMargin (in DXA)
// US Letter with 0.5" margins: 12240 - 1440 = 10800
const contentWidth = 10800;

twoColRow(
  [new TextRun({ text: "Northeastern University", bold: true, font: "Times New Roman", size: 20 })],
  [new TextRun({ text: "Boston, MA", bold: true, font: "Times New Roman", size: 20 })],
  contentWidth
);
```

## Other Google Docs Compatibility Rules

1. **Always use `WidthType.DXA`** for table widths. `WidthType.PERCENTAGE` breaks in Google Docs.
2. **Set both `columnWidths` on the table AND `width` on each cell.** Both must match.
3. **Use `ShadingType.CLEAR`**, never `SOLID`, for table cell shading.
4. **Avoid em dashes** (`\u2013`, `\u2014`). Use commas, hyphens, or reword instead. Google Docs sometimes renders these inconsistently across fonts.
5. **Never use `\n` for line breaks.** Use separate `Paragraph` elements.
6. **Never use unicode bullet characters directly.** Use `LevelFormat.BULLET` with numbering config.

## When This Skill Applies

Apply these rules to ALL .docx output by default. Most users open .docx files in Google Docs, not Microsoft Word. Even if the user doesn't mention Google Docs, use invisible tables over tab stops as a defensive measure. There is zero visual difference in Word, but it prevents breakage in Google Docs.
