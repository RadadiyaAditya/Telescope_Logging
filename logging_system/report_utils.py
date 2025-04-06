from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def generate_pdf_reportlab(session_data, filepath):
    doc = SimpleDocTemplate(filepath, pagesize=landscape(A4), rightMargin=1*cm, leftMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    title_style.fontSize = 16
    story.append(Paragraph(f"Session Details: {session_data['session_id']}", title_style))
    story.append(Spacer(1, 12))

    # Section header style
    section_title = ParagraphStyle(
        'SectionHeader', fontSize=10, leading=12, alignment=1,
        spaceAfter=6, spaceBefore=6, fontName='Helvetica-Bold', textTransform='uppercase'
    )

    table_style = TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.whitesmoke),
        ('TEXTCOLOR', (0,0), (0,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ])

    def make_table(data):
        return Table(data, colWidths=[3.5*cm, 5.3*cm], style=table_style, hAlign='CENTER')

    def add_row(title_row, data_row):
        title_with_spacing = [title_row[0], "", title_row[1], "", title_row[2]]
        data_with_spacing = [data_row[0], "", data_row[1], "", data_row[2]]

        story.append(Table([title_with_spacing], colWidths=[8.5*cm, 0.5*cm, 8.5*cm, 0.5*cm, 9*cm], style=[('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        story.append(Spacer(1, 8))
        story.append(Table([data_with_spacing], colWidths=[8.5*cm, 0.5*cm, 8.5*cm, 0.5*cm, 9*cm], style=[
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(Spacer(1, 36))

    # Row 1
    add_row([
        Paragraph("General Information", section_title),
        Paragraph("Weather Parameters", section_title),
        Paragraph("Observation Parameters", section_title)
    ], [
        make_table([
            ["Telescope", session_data['general']['telescope_name']],
            ["Operator", session_data['general']['telescope_operator']],
            ["Observer", session_data['general']['observer_name']],
            ["Log Start (UTC)", session_data['general']['log_start_time_utc']],
            ["Log Start (LST)", session_data['general']['log_start_time_lst']],
            ["Log End (UTC)", session_data['general']['log_end_time_utc']],
            ["Log End (LST)", session_data['general']['log_end_time_lst']],
        ]),
        make_table([
            ["Temperature (°C)", session_data['weather']['temperature']],
            ["Humidity", session_data['weather']['humidity']],
            ["Wind Speed", session_data['weather']['wind_speed']],
            ["Seeing", session_data['weather']['seeing']],
            ["Cloud Cover", session_data['weather']['cloud_coverage']],
            ["Moon Phase", session_data['weather']['moon_phase']],
        ]),
        make_table([
            ["Target", session_data['observation']['target_name']],
            ["Right Ascension", session_data['observation']['right_ascension']],
            ["Declination", session_data['observation']['declination']],
            ["Magnitude", session_data['observation']['magnitude']],
        ])
    ])

    # Row 2
    add_row([
        Paragraph("Telescope Configuration", section_title),
        Paragraph("Instrumentation", section_title),
        Paragraph("Remote Operation", section_title)
    ], [
        make_table([
            ["Focus Position", session_data['telescope']['focus_position']],
            ["Air Mass", session_data['telescope']['air_mass']],
            ["Tracking Mode", session_data['telescope']['tracking_mode']],
            ["Guiding Status", session_data['telescope']['guiding_status']],
        ]),
        make_table([
            ["Instrument", session_data['instrument']['instrument_name']],
            ["Observing Mode", session_data['instrument']['observing_mode']],
            ["Calibration", session_data['instrument']['calibration']],
            ["Filter", session_data['instrument']['filter_in_use']],
            ["Exposure Time", session_data['instrument']['exposure_time']],
            ["Polarization Mode", session_data['instrument']['polarization_mode']],
        ]),
        make_table([
            ["Remote Access", session_data['remote']['remote_access']],
            ["Remote Observer", session_data['remote']['remote_observer']],
            ["Emergency Stop", session_data['remote']['emergency_stop']],
        ])
    ])

    # Row 3 - Comments only in center
    comment_text = session_data['comments']['comments']
    comment_para = Paragraph(comment_text, styles['Normal'])
    comment_table = Table(
    [["Comments", comment_para]],
    colWidths=[3 * cm, 25 * cm],
    style=[
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, 0), colors.whitesmoke)
    ]
    )

    story.append(Spacer(1, 12))
    story.append(Paragraph("Comments", section_title))
    story.append(Spacer(1, 6))
    story.append(KeepTogether(comment_table))
    
    doc.build(story)
