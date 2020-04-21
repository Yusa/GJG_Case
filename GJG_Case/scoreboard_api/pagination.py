from rest_framework.pagination import PageNumberPagination
from GJG_Case.scoreboard_api.models import User
from django.core.paginator import Paginator, Page

# Original Paginator was not working efficiently since it was storing all of the rows from table
# and then does the following operation while returning page: self.object_list[bottom:top]
# Instead of this approach, I wrote the paginator which gets only the necessary part from database 
class CustomPaginator(Paginator):
	country_code = None

	def page(self, number):
		"""Return a Page object for the given 1-based page number."""
		number = self.validate_number(number)

		where_str = ""
		if self.country_code != None:
			where_str = f"WHERE country = '{self.country_code}'"


		# Query is made with both ways to reduce slowing when reaching high pages
		if number <= self.num_pages/2:
			query_str = """SELECT * from scoreboard_api_user """ + where_str + """ order by points DESC, rank
								offset %s rows
								FETCH NEXT %s rows only
								"""
			res = User.objects.raw(query_str, [(number - 1) * self.per_page, self.per_page])

		else:
			query_str = """SELECT * from scoreboard_api_user """ + where_str + """ order by points ASC, rank DESC 
								offset %s rows
								FETCH NEXT %s rows only
								"""
			res = User.objects.raw(query_str, [(self.num_pages - number) * self.per_page, self.per_page])[::-1]
		return self._get_page(res, number, self)


	def _get_page(self, *args, **kwargs):
		"""
		Return an instance of a single page.
		This hook can be used by subclasses to use an alternative to the
		standard :cls:`Page` object.
		"""
		return Page(*args, **kwargs)



class LeaderboardPagination(PageNumberPagination):
	page_size = 20
	page_number = 1
	django_paginator_class = CustomPaginator

	def paginate_queryset(self, queryset, request, country_code=None, view=None):
		"""
		Paginate a queryset if required, either returning a
		page object, or `None` if pagination is not configured for this view.
		"""

		page_size = self.get_page_size(request)

		if not page_size:
			return None

		paginator = self.django_paginator_class(queryset, page_size)
		if country_code != None:
			paginator.country_code = country_code

		page_number = request.query_params.get(self.page_query_param, 1)

		if page_number in self.last_page_strings:
			page_number = paginator.num_pages

		try:
			self.page = paginator.page(page_number)

		except Exception as e:
			raise Exception("Page number is not valid.")

		self.request = request
		result = list(self.page)
		return result
