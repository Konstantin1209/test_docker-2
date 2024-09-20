from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

    def validate(self, data):
        if not data.get('product'):
            raise serializers.ValidationError({'Ошибка'})
        return data


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, read_only=False)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            try:
                StockProduct.objects.create(stock=stock, **position)
            except Exception as e:
                raise serializers.ValidationError({'positions': str(e)})
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            try:
                obj, created = StockProduct.objects.get_or_create(stock=stock, product=position['product'])
                obj.quantity = position['quantity']
                obj.price = position['price']
                obj.save()
            except Exception as e:
                raise serializers.ValidationError({'positions': str(e)})
        return stock
