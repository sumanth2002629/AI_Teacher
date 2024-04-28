from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

def wrap_text(text, max_width):
    words = text.split()
    lines = []
    current_line = ''

    for word in words:
        if stringWidth(current_line + ' ' + word, "Helvetica", 12) <= max_width:  # Providing default font name and font size
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def write_list_to_pdf(file_name, strings):
    # Create a PDF file
    pdf_file = open(file_name, 'wb')

    # Create a canvas
    pdf_canvas = canvas.Canvas(pdf_file, pagesize=letter)

    # Set starting position and other parameters
    x = 100
    y = 750
    max_width = 400
    max_height = 750
    leading = 12

    # Iterate over the list of strings and write each string to the PDF
    for string in strings:
        # Split the string into lines that fit within the maximum width
        lines = wrap_text(string, max_width)

        # Check if adding these lines would exceed the max height
        if y - (len(lines) * leading) < 50:  # Assuming a margin of 50 units from the bottom
            pdf_canvas.showPage()  # Move to the next page
            y = max_height  # Reset y-coordinate for the new page

        # Draw the lines on the canvas
        for line in lines:
            pdf_canvas.drawString(x, y, line.strip())
            y -= leading  # Move to the next line

    # Save the canvas content
    pdf_canvas.save()

    # Close the file
    pdf_file.close()

# Example list of strings
if __name__=="__main__":
    strings = [
        "First line of text",
        "Second line of text",
        "A very long sentence that should wrap to the next line because it exceeds the maximum width of the page.",
        "Fourth line of text",
        "Fifth line of text",
        "Sixth line of text"
    ]

    # Write the list of strings to a PDF file
    write_list_to_pdf('output.pdf', strings)

    print("PDF created successfully!")
