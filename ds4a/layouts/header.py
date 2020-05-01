import dash_html_components as html

LOGO_LOGGI = "/assets/images/loggi-logo.png"
LOGO_CO = "/assets/images/co-logo.png"
MINI_LOGGI = "/assets/images/loggi-mini.png"
MINI_CO = "/assets/images/co-mini.png"

header = html.Div(
    [
        html.Div('', className='header-top'),

        html.Div(html.A(html.Img(src=LOGO_LOGGI), href="/",), className='loggi-logo col-lg-4'),
        html.Div(html.A(html.Img(src=MINI_LOGGI), href="/",), className='loggi-mini col-2'),

        html.Div('Last Mile Dashboard', className='dashboard-title col-lg-4 col-sm-8 col-8'),

        html.Div(html.A(html.Img(src=LOGO_CO), href="/",), className='co-logo col-lg-4'),
        html.Div(html.A(html.Img(src=MINI_CO), href="/",), className='co-mini col-2'),

        html.Div('', className='header-bottom'),
    ],
    className='header'
)