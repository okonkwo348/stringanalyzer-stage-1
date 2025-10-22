from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from .utils import analyze_string

class AnalyzeStringView(APIView):
    def post(self, request):
        value = request.data.get("value")

        # Missing field
        if value is None:
            return Response({"error": "Missing 'value' field"}, status=400)

        # Invalid type
        if not isinstance(value, str):
            return Response({"error": "'value' must be a string"}, status=422)

        analysis = analyze_string(value)

        # Duplicate check
        if AnalyzedString.objects.filter(sha256_hash=analysis["sha256_hash"]).exists():
            return Response({"error": "String already exists"}, status=409)

        data = {**analysis, "value": value}
        serializer = AnalyzedStringSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "id": analysis["sha256_hash"],
            "value": value,
            "properties": analysis,
            "created_at": now().isoformat()
        }, status=201)

class GetStringView(APIView):
    def get(self, request, value):
        try:
            string_obj = AnalyzedString.objects.get(value=value)
        except AnalyzedString.DoesNotExist:
            return Response({"error": "String not found"}, status=404)

        serializer = AnalyzedStringSerializer(string_obj)
        return Response({
            "id": string_obj.sha256_hash,
            "value": string_obj.value,
            "properties": {
                "length": string_obj.length,
                "is_palindrome": string_obj.is_palindrome,
                "unique_characters": string_obj.unique_characters,
                "word_count": string_obj.word_count,
                "sha256_hash": string_obj.sha256_hash,
                "character_frequency_map": string_obj.character_frequency_map,
            },
            "created_at": string_obj.created_at.isoformat()
        }, status=200)

class GetStringsView(APIView):
    def get(self, request):
        qs = AnalyzedString.objects.all()
        filters_applied = {}

        try:
            is_palindrome = request.GET.get("is_palindrome")
            if is_palindrome is not None:
                filters_applied["is_palindrome"] = is_palindrome.lower() == "true"
                qs = qs.filter(is_palindrome=filters_applied["is_palindrome"])

            min_length = request.GET.get("min_length")
            if min_length:
                filters_applied["min_length"] = int(min_length)
                qs = qs.filter(length__gte=int(min_length))

            max_length = request.GET.get("max_length")
            if max_length:
                filters_applied["max_length"] = int(max_length)
                qs = qs.filter(length__lte=int(max_length))

            word_count = request.GET.get("word_count")
            if word_count:
                filters_applied["word_count"] = int(word_count)
                qs = qs.filter(word_count=int(word_count))

            contains_character = request.GET.get("contains_character")
            if contains_character:
                filters_applied["contains_character"] = contains_character
                qs = [q for q in qs if contains_character in q.value]
        except ValueError:
            return Response({"error": "Invalid query parameter types"}, status=400)

        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "count": len(serializer.data),
            "filters_applied": filters_applied
        }, status=200)

class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.GET.get("query")
        if not query:
            return Response({"error": "Missing query"}, status=400)

        parsed_filters = {}
        qs = AnalyzedString.objects.all()
        q = query.lower()

        if "palindromic" in q:
            parsed_filters["is_palindrome"] = True
            qs = qs.filter(is_palindrome=True)

        if "single word" in q:
            parsed_filters["word_count"] = 1
            qs = qs.filter(word_count=1)

        if "longer than" in q:
            try:
                num = int(q.split("longer than")[1].split()[0])
                parsed_filters["min_length"] = num + 1
                qs = qs.filter(length__gt=num)
            except:
                return Response({"error": "Unable to parse length"}, status=400)

        if "containing the letter" in q:
            char = q.split("letter")[-1].strip()[0]
            parsed_filters["contains_character"] = char
            qs = [s for s in qs if char in s.value]

        if not parsed_filters:
            return Response({"error": "Unable to parse query"}, status=400)

        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response({
            "data": serializer.data,
            "count": len(serializer.data),
            "interpreted_query": {
                "original": query,
                "parsed_filters": parsed_filters
            }
        }, status=200)

class DeleteStringView(APIView):
    def delete(self, request, value):
        try:
            obj = AnalyzedString.objects.get(value=value)
            obj.delete()
            return Response(status=204)
        except AnalyzedString.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

