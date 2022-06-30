from carro.carro import Carro


def importe_total_carro(request):
    carro = Carro(request)
    total = 0
    total_prod = 0
    print(request.session)
    if request.user.is_authenticated:
        for key, value in request.session["carro"].items():
            total = total+(int(value["precio"]))
            total_prod = total_prod+(int(value["cantidad"]))
    return {"importe_total_carro": total,"cantidad_prod":total_prod}
