Read the PDF file that the user has referenced in their most recent message (or the file currently open in their editor). Use the `breakup_big_pdf` skill first to check page count, then extract text from the PDF using pypdf.

Scan the extracted text for all assignments with due dates. Output a markdown table with two columns:

| Due Date | Assignment |
|---|---|

Sort rows from earliest to latest due date. Include every assignment, bloggy, response, rough draft, revision club item, and final draft found. Format dates consistently (e.g., "Thu, Feb 26, 11:59 PM"). If a date range is found (like Spring Break), include it as-is.

Do not include any other commentary — just the table.
