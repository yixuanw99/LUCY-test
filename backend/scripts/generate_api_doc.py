import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_api_pdf(openapi_json_path, output_pdf_path):
    '''
    # Usage
    openapi_json_path = 'D:/Downloads/openapi.json'
    output_pdf_path = 'D:/Downloads/api_documentation.pdf'
    generate_api_pdf(openapi_json_path, output_pdf_path)
    '''
    # Load OpenAPI JSON
    with open(openapi_json_path, 'r') as f:
        openapi_spec = json.load(f)

    # Create PDF
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(openapi_spec['info']['title'], styles['Title']))
    story.append(Spacer(1, 12))

    # Description
    if 'description' in openapi_spec['info']:
        story.append(Paragraph(openapi_spec['info']['description'], styles['Normal']))
        story.append(Spacer(1, 12))

    # Endpoints
    for path, path_item in openapi_spec['paths'].items():
        for method, operation in path_item.items():
            # Endpoint title
            story.append(Paragraph(f"{method.upper()} {path}", styles['Heading2']))
            story.append(Spacer(1, 6))

            # Summary and description
            if 'summary' in operation:
                story.append(Paragraph(operation['summary'], styles['Normal']))
            if 'description' in operation:
                story.append(Paragraph(operation['description'], styles['Normal']))
            story.append(Spacer(1, 6))

            # Parameters
            if 'parameters' in operation:
                story.append(Paragraph("Parameters:", styles['Heading4']))
                param_data = [["Name", "In", "Required", "Description"]]
                for param in operation['parameters']:
                    param_data.append([
                        param['name'],
                        param['in'],
                        str(param.get('required', False)),
                        param.get('description', '')
                    ])
                t = Table(param_data, colWidths=[80, 50, 60, 300])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(t)
                story.append(Spacer(1, 12))

            # Responses
            if 'responses' in operation:
                story.append(Paragraph("Responses:", styles['Heading4']))
                for status, response in operation['responses'].items():
                    story.append(Paragraph(f"{status}: {response.get('description', '')}", styles['Normal']))

            story.append(Spacer(1, 12))

    doc.build(story)

def generate_swagger_html(openapi_json_path, output_path):
    '''
    # Usage
    openapi_json_path = 'D:/Downloads/openapi_v3.0.3.json'
    output_path = 'D:/Downloads/swagger-ui.html'
    generate_swagger_html(openapi_json_path, output_path)
    '''
    # Read the OpenAPI JSON
    with open(openapi_json_path, 'r') as f:
        openapi_spec = json.load(f)
    
    # Ensure the spec has a valid version
    if 'swagger' not in openapi_spec and 'openapi' not in openapi_spec:
        openapi_spec['openapi'] = '3.0.3'  # Add a default version if missing
    
    # Create the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css" >
        <style>
            html {{
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }}
            
            *,
            *:before,
            *:after {{
                box-sizing: inherit;
            }}
            
            body {{
                margin:0;
                background: #fafafa;
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.min.js"> </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-standalone-preset.min.js"> </script>
        <script>
        window.onload = function() {{
          const ui = SwaggerUIBundle({{
            spec: {json.dumps(openapi_spec)},
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
              SwaggerUIBundle.presets.apis,
              SwaggerUIStandalonePreset
            ],
            plugins: [
              SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "BaseLayout"
          }})
          window.ui = ui
        }}
        </script>
    </body>
    </html>
    """
    
    # Write the HTML file
    with open(output_path, 'w') as f:
        f.write(html_content)


# Usage
openapi_json_path = 'D:/Downloads/openapi.json'
output_pdf_path = 'D:/Downloads/api_documentation.pdf'
generate_api_pdf(openapi_json_path, output_pdf_path)

openapi_json_path = 'D:/Downloads/openapi_v3.0.3.json' # openapi的版本要改成3.0.n才能直接用html，所以另存了一個openapi_v3.0.3.json
output_path = 'D:/Downloads/swagger-ui.html'
generate_swagger_html(openapi_json_path, output_path)