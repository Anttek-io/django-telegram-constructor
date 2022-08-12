from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from administration.models import Department, Position


class ParentDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name',)


class DepartmentSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super(DepartmentSerializer, self).get_fields()
        fields.update([
            ('parent_department', ParentDepartmentSerializer(read_only=True)),
            ('parent_department_id', serializers.PrimaryKeyRelatedField(
                queryset=Department.objects.all(), write_only=True, source='parent_department'))])
        return fields

    def validate(self, attrs):
        if 'parent_department' in attrs:
            parent_department = attrs['parent_department']
            if parent_department.pk == self.instance.pk:
                raise serializers.ValidationError(
                    {'parent_department': _('You cannot set the department itself as it\'s parent')}
                )
            # TODO: Продумать грамотную проверку на то, что объект не удален и активен.
        return attrs

    class Meta:
        model = Department
        fields = '__all__'
        depth = 1


class ParentPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name',)


class PositionSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super(PositionSerializer, self).get_fields()
        fields.update([
            ('parent_position', ParentPositionSerializer(read_only=True)),
            ('parent_position_id', serializers.PrimaryKeyRelatedField(
                queryset=Position.objects.all(), write_only=True, source='parent_position'))])
        return fields

    def validate(self, attrs):
        if 'parent_position' in attrs:
            parent_position = attrs['parent_position']
            if parent_position.pk == self.instance.pk:
                raise serializers.ValidationError(
                    {'parent_position': _('You cannot set the position itself as it\'s parent')}
                )
            # TODO: Продумать грамотную проверку на то, что объект не удален и активен.
        return attrs

    class Meta:
        model = Position
        fields = '__all__'
        depth = 1
