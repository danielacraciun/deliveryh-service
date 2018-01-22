from rest_framework import serializers

from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):

    opens_at = serializers.TimeField(
        format="%H:%M", help_text="The opening hour, in 24-hour clock format"
    )
    closes_at = serializers.TimeField(
        format="%H:%M", help_text="The closing hour, in 24-hour clock format"
    )

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'opens_at', 'closes_at')

    def validate(self, data):
        """
        Check that the open time is before the closing time.
        """
        opens_at = data.get(
            'opens_at', self.instance.opens_at if self.instance else None
        )
        closes_at = data.get(
            'closes_at', self.instance.closes_at if self.instance else None
        )

        if opens_at and closes_at and opens_at > closes_at:
            raise serializers.ValidationError(
                "Restaurant cannot have a closing time before an opening time"
            )

        return data
