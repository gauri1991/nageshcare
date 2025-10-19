"""
Simple test WSGI application to verify Passenger/cPanel configuration.
Temporarily rename this to passenger_wsgi.py to test if the server is working.

If this works, the issue is with your Django app, not the server setup.
"""

def application(environ, start_response):
    """
    Minimal WSGI application for testing.
    """
    import sys
    import os

    # Build response
    output = []
    output.append("=" * 80)
    output.append("PASSENGER WSGI TEST - SUCCESS!")
    output.append("=" * 80)
    output.append("")
    output.append("If you see this page, Passenger is working correctly.")
    output.append("The issue is likely with your Django application.")
    output.append("")
    output.append("-" * 80)
    output.append("SYSTEM INFORMATION")
    output.append("-" * 80)
    output.append(f"Python Version: {sys.version}")
    output.append(f"Python Executable: {sys.executable}")
    output.append(f"Script Location: {os.path.dirname(os.path.abspath(__file__))}")
    output.append("")
    output.append("-" * 80)
    output.append("ENVIRONMENT VARIABLES")
    output.append("-" * 80)

    # Show some environment variables
    interesting_vars = [
        'DJANGO_ENV',
        'PYTHONPATH',
        'PATH',
        'PWD',
        'HOME',
        'USER',
    ]

    for var in interesting_vars:
        value = os.environ.get(var, 'NOT SET')
        output.append(f"{var} = {value}")

    output.append("")
    output.append("-" * 80)
    output.append("WSGI ENVIRONMENT")
    output.append("-" * 80)
    output.append(f"Request Method: {environ.get('REQUEST_METHOD', 'N/A')}")
    output.append(f"Path Info: {environ.get('PATH_INFO', 'N/A')}")
    output.append(f"Query String: {environ.get('QUERY_STRING', 'N/A')}")
    output.append(f"Server Name: {environ.get('SERVER_NAME', 'N/A')}")
    output.append(f"Server Port: {environ.get('SERVER_PORT', 'N/A')}")
    output.append("")
    output.append("=" * 80)
    output.append("")
    output.append("NEXT STEPS:")
    output.append("1. Rename this file back to test_wsgi.py")
    output.append("2. Restore your original passenger_wsgi.py")
    output.append("3. Run: python diagnose_app.py")
    output.append("4. Fix any errors found in the diagnostic")
    output.append("5. Restart the Python app in cPanel")
    output.append("")

    response_body = "\n".join(output)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain; charset=utf-8'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode('utf-8')]
