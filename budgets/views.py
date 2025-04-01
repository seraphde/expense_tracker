from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Budget
from .serializers import BudgetSerializers
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from expenses.models import Expense
from decimal import Decimal


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def budget_list_create(request):
    if request.method == 'GET':
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializers(budgets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BudgetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def budget_detail(request, pk):
    try:
        budget = Budget.objects.get(pk=pk, user=request.user)
    except Budget.DoesNotExist:
        return Response({"error": "budget not found "}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BudgetSerializers(budget)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BudgetSerializers(budget, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        budget.delete()
        return Response({"message": "budget deleted! "}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def budgets_progress(request, pk):
    try:
        budget = Budget.objects.get(pk=pk, user=request.user)
    except Budget.DoesNotExist:
        return Response({'error': 'Budget not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    aggregate_result = Expense.objects.filter(
        user=request.user,
        date__gte=budget.start_date,
        date__lte=budget.end_date
    ).aggregate(total=Sum('amount'))

    total_spent = aggregate_result['total'] or 0  
    total_spent_decimal = Decimal(str(total_spent))  
    
    remaining = budget.amount - total_spent_decimal 

    return Response({
        'budget': BudgetSerializers(budget).data,  
        'total_spent': total_spent,
        'remaining': budget.amount - total_spent
    })

