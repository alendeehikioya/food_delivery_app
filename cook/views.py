from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from django.shortcuts import render
from django.views import View
from customer.models import MenuItem, OrderModel
from customer.views import Order




class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.get_cart_total

            if not order.is_shipped:
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'cook/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'price': order.get_cart_total,
            'order': order
        }

        return render(request, 'cook/order_details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'cook/order_details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()

