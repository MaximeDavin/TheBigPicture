from rest_framework.viewsets import ModelViewSet
from api.models import BigPicture, Rating, SUBJECT_CODE
from api.serializers import BigPictureSerializer
from api.permissions import IsAuthorOrReadOnly
import json
import datetime


class SubjectViewSet(ModelViewSet):
	queryset = BigPicture.objects.filter(kind=SUBJECT_CODE).order_by('-modification_date')
	serializer_class = BigPictureSerializer
	permission_classes = [IsAuthorOrReadOnly]

	def get_serializer_context(self):
		context = super(SubjectViewSet, self).get_serializer_context()
		context.update({
			"author": context["request"].user.id,
			"target": context["request"].query_params.get('ratingauthor', None)
		})
		return context

	def get_queryset(self):
		queryset = self.queryset
		author = self.request.query_params.get('author', None)
		ratingauthor = self.request.query_params.get('ratingauthor', None)
		reference = self.request.query_params.get('reference', None)
		if reference is not None:
			references = BigPicture.objects.get(id=reference).references.all().distinct('subject').values('subject')
			queryset = queryset.filter(id__in=[r["subject"] for r in references])
		if author is not None:
			queryset = queryset.filter(author=author)
		if ratingauthor is not None:
			ratings = Rating.objects.filter(author_id=ratingauthor).distinct('subject').values('subject')
			queryset = queryset.filter(id__in=[r["subject"] for r in ratings]).exclude(author_id=ratingauthor)
		return queryset


class BigPictureViewSet(ModelViewSet):
	queryset = BigPicture.objects.all().order_by('-modification_date')
	serializer_class = BigPictureSerializer
	permission_classes = [IsAuthorOrReadOnly]

	def get_queryset(self):
		queryset = self.queryset
		element = self.request.query_params.get('element', None)
		if element is not None:
			elt = queryset.get(id=element)
			queryset = queryset.filter(parent=element)
			if elt.parent is not None:
				context = BigPicture.objects.filter(id=elt.parent.id)
				queryset |= context
		return queryset

	def get_serializer_context(self):
		context = super(BigPictureViewSet, self).get_serializer_context()
		context.update({
			"author": context["request"].user.id,
			"target": context["request"].query_params.get('ratingauthor', None)
		})
		return context

	def create(self, request):
		request.data["author_id"] = request.user.id
		if "subject" in request.data and request.data["subject"] is not None:
			subject = BigPicture.objects.get(id=request.data["subject"])
			parent = BigPicture.objects.get(id=request.data["parent"])
			assert subject.author.id == request.user.id
			assert parent.author.id == request.user.id
			assert parent.id == subject.id or subject.id == parent.subject.id
		else:
			assert request.data["kind"] == SUBJECT_CODE
		return super().create(request)