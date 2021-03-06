from rest_framework import serializers


class MarketSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    total_market_cap = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(required=False)
    turnover = serializers.FloatField(required=False)
    pe = serializers.FloatField(required=False)
    date = serializers.CharField(required=False)


@DeprecationWarning
class MarketOverallSerializer(serializers.Serializer):
    # markets = MarketSerializer(many=True)  # A nested list of 'edit' items.
    sh = MarketSerializer()
    sz = MarketSerializer()
    cyb = MarketSerializer()
    zxb = MarketSerializer()


class MarketsSerializer(serializers.Serializer):
    markets = MarketSerializer(many=True)  # A nested list of 'edit' items.


class AhSerializer(serializers.Serializer):
    value = serializers.FloatField(read_only=True)
    date = serializers.CharField(required=False)


class AhIndexSerializer(serializers.Serializer):
    items = AhSerializer(many=True)  # A nested list of 'edit' items.


class SwSerializer(serializers.Serializer):
    BargainDate = serializers.IntegerField(required=False)
    PB = serializers.FloatField(read_only=True)
    PE = serializers.FloatField(read_only=True)


class SwIndexSerializer(serializers.Serializer):
    items = SwSerializer(many=True)  # A nested list of 'edit' items.


class StockSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    close = serializers.FloatField(read_only=True)
    volume = serializers.FloatField(read_only=True)
    timestamp = serializers.IntegerField(read_only=True)
    turn_rate = serializers.FloatField(read_only=True)

class StockListSerializer(serializers.Serializer):
    items = StockSerializer(many=True)  # A nested list of 'edit' items.


class CixSerializer(serializers.Serializer):
    value = serializers.FloatField(read_only=True)
    timestamp = serializers.IntegerField(required=False)


class CixListSerializer(serializers.Serializer):
    items = CixSerializer(many=True)  # A nested list of 'edit' items.