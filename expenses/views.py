from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from .models import Expense
from django.db.models import Sum
from .serializers import ExpenseSerializer
from datetime import timedelta
from django.utils import timezone



@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password2 = request.data.get('password2')

        if not username or not email or not password or not password2:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if password != password2:
            return Response({"error": "the password doesnt match "}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "username exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "successfully created "}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_page(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'login successfuly',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid Credentials'}, status=400)
    
@api_view(['POST'])
def logout_page(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=200)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=400)




@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def expense_list_create(request):
    if request.method == 'GET':
        catagory = request.query_params.get('catagory', None)
        expenses = Expense.objects.filter(user=request.user)
        if catagory:
            expenses = expenses.filter(catagory=catagory)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def expense_detail(request, pk):
    try: 
        expense = Expense.objects.get(pk=pk, user=request.user)
    except Expense.DoesNotExist:
        return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        expense.delete()
        return Response({'message':' Expense deletede}'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def weekly_summary(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_expenses = Expense.objects.filter(
        user=request.user,
        date__gte=start_of_week,
        date__lte=end_of_week
    ).aggregate(total=Sum('amount'))['total'] or 0.00

    return Response({
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'total_expenses': weekly_expenses
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monthly_summary(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__gte=start_of_month,
        date__lte=end_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0.00

    return Response({
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'totalexpenses': monthly_expenses
    })