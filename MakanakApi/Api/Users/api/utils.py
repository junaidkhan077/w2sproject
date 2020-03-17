
def get_client_masked_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if not x_forwarded_for:
        ip = request.META.get('REMOTE_ADDR')

    elif ',' in x_forwarded_for:
        ip = x_forwarded_for.split(',')[-2]

    else:
        ip = x_forwarded_for

    ip = ip.strip()
    ip = '.'.join(ip.split('.')[:-1]) + '.0'
    return ip
