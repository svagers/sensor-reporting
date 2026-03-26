from django.shortcuts import render


def welcome_page(request):
    """HTML welcome screen with links to OpenAPI schema, Swagger UI, and API info."""
    return render(request, "api/welcome_page.html")
