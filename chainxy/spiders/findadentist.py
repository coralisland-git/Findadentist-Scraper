# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from lxml import etree

from lxml import html

import time

import pdb

import random


class Findadentist(scrapy.Spider):

	name = 'findadentist'

	domain = 'https://findadentist.ada.org/'

	history = []

	output = []

	request_log = []

	def __init__(self):

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/US_Cities.json'

		with open(file_path) as data_file:    

			self.location_list = json.load(data_file)

		script_dir = os.path.dirname(__file__)

		file_path = script_dir + '/proxies.txt'

		with open(file_path, 'rb') as text:

			self.proxy_list =  [ "http://" + x.strip() for x in text.readlines()]

	
	def start_requests(self):

		for location in self.location_list:

			url = 'https://findadentist.ada.org/api/Dentists?Address='+location['city']+'&Distance=100'

			headers = {

				"Accept": "application/json, text/plain, */*",

				"Accept-Encoding": "gzip, deflate, br",

				"Authorization": "Basic NUNtQitIcVZuOXhTVnFKNkhiZC8xSGZnb29NdU1ZaXk=",

				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
			}

			yield scrapy.Request(url, headers=headers, callback=self.parse, meta={'proxy' : random.choice(self.proxy_list)}) 


	def parse(self, response):

		dentist_list = json.loads(response.body)

		for dentist in dentist_list:

			person_id = dentist['PersonId']

			address_id = dentist['AddressId']

			link = 'https://findadentist.ada.org/api/DentistProfile?PersonId='+str(person_id)+'&AddressId='+str(address_id)

			if link not in self.history:

				self.history.append(link)

				headers = {

					'Accept': 'application/json, text/plain, */*',

					'Accept-Encoding': 'gzip, deflate, br',

					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
				}

				yield scrapy.Request(link, headers=headers, callback=self.parse_detail, meta={'proxy' : random.choice(self.proxy_list)})


	def parse_detail(self, response):

		dentist = json.loads(response.body)

		item = ChainItem()

		item['name'] = self.validate(dentist['Name'])

		item['email'] = self.validate(dentist['Email'])

		item['phone'] = self.validate(dentist['Phone'])

		item['website'] = self.validate(dentist['WebSite'])

		item['address1'] = self.validate(dentist['AddressLine1'])

		item['address2'] = self.validate(dentist['AddressLine2'])

		item['city'] = self.validate(dentist['City'])

		item['state'] = self.validate(dentist['State'])

		item['zipcode'] = self.validate(dentist['Zip'])

		item['photo'] = self.validate(dentist['Photo'])

		item['specialty'] = self.validate(dentist['Specialty'])

		item['latitude'] = self.validate(str(dentist['Latitude']))

		item['longitude'] = self.validate(str(dentist['Longitude']))

		if item['city'] == None:

			headers = {

				'Accept': 'application/json, text/plain, */*',

				'Accept-Encoding': 'gzip, deflate, br',

				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
			}

			if self.count(response.url, self.request_log) < 3:

				yield scrapy.Request(response.url, headers=headers, callback=self.parse_detail, meta={'proxy' : random.choice(self.proxy_list)}, dont_filter=True)

				self.request_log.append(response.url)

		else:

			yield item


	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp

	def count(self, item, arr):

		num = 0

		for tmp in arr:

			if tmp == item:

				num += 1

		return num