async def should_abort_request(request):
      if request.resource_type in ["media", "font", "image"]:
            return True
      return False
