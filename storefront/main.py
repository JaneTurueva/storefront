from aiohttp import web

class CompaniesView(web.View):
    async def post(self):
        return web.Response(text='Create and return company')

    async def get(self):
        return web.json_response(data=[{'id': 1}])


class CompanyView(web.View):
    @property
    def company_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> web.Response:
        return web.Response(text='Get one company by id %r' % self.company_id)

    async def put(self) -> web.Response:
        return web.Response(text='Update company by id %r' % self.company_id)

    async def delete(self) -> web.Response:
        return web.Response(text='Delete company by id %r' % self.company_id)


class EmployeesView(web.View):
    async def post(self):
        return web.Response(text='Create and return employee')

    async def get(self):
        return web.Response(text='Get employees')


class EmployeeView(web.View):
    @property
    def employee_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self) -> web.Response:
        return web.Response(text='Get one employee by id %r' % self.employee_id)

    async def put(self) -> web.Response:
        return web.Response(
            text='Update one employee by id %r' % self.employee_id
        )

    async def delete(self) -> web.Response:
        return web.Response(
            text='Delete one employee by id %r' % self.employee_id
        )


class ProductsView(web.View):
    async def post(self):
        return web.Response(text='Create and return product')

    async def get(self):
        return web.Response(text='Get products')


class ProductView(web.View):
    @property
    def product_id(self) -> int:
        return int(self.request.match_info['id'])

    async def get(self):
        return web.Response(text='Get one product by id %r' % self.product_id)

    async def put(self):
        return web.Response(text='Update productby by id %r' % self.product_id)

    async def delete(self):
        return web.Response(text='Delete product by id %r' % self.product_id)


def main():
    app = web.Application()
    app.router.add_route('*', '/companies', CompaniesView)
    app.router.add_route('*', '/companies/{id}', CompanyView)
    app.router.add_route('*', '/employees', EmployeesView)
    app.router.add_route('*', '/employees/{id}', EmployeeView)
    app.router.add_route('*', '/products', ProductsView)
    app.router.add_route('*', '/products/{id}', ProductView)
    web.run_app(app)