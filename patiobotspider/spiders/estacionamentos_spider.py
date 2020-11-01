import scrapy
from scrapy import Request
import datetime
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.utils.response import open_in_browser
import re


x = datetime.datetime.now()
if x.strftime("%m") == '12':
    hoje = str(int(x.strftime("%Y")) + 1)+"-" + "01" + "-" + "01"

    semana_q_vem = str(int(x.strftime("%Y")) + 1)+"-" + "01" + "-" + "06"
else:

    hoje = x.strftime("%Y")+"-" + str(int(x.strftime("%m"))+1).zfill(2)+"-" + "01"

    semana_q_vem = x.strftime("%Y")+"-" + str(int(x.strftime("%m"))+1).zfill(2)+"-" + "06"


from shutil import which

SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS=['-headless']

from scrapy_selenium import SeleniumRequest

class EstacionamentosSpider(scrapy.Spider):
    name = "patiobot"
    start_urls = [
        'http://veloxpark.com.br/tarifas-e-promocoes/',
        'https://site.bh-airport.com.br/SitePages/pt/estacionamento/index.aspx',
        'http://www.parkconfins.com.br/',
        'http://www.superparkestacionamento.com.br/',
        'https://www.estacionamentospacepark.com.br/',
        'https://www.centralparkconfins.com.br/tarifas',
        'https://www.estapar.com.br/reserva-de-vaga/horarios?codigo=2203&pid=null&data-entrada='+ hoje + '&data-saida=' + hoje + '&pc=null&parceiro=null',
        'http://www.bpark.com.br/',
        'https://www.parebem.com.br/estacionamento/estacionamento-aeroporto-de-confins/',
        'https://www.autoparkbrasil.com.br/',
        'https://estacionamentopatioconfins.com.br/wp/preco-estacionamento-aeroporto-de-confins/'
        #'http://www.greenlinepark.com.br/'
    ]

    def parse(self, response):
        if response.url == "http://veloxpark.com.br/tarifas-e-promocoes/":



            yield {
            'nome': 'Velox',
            'logo': 'http://veloxpark.com.br/site-wp-vp/wp-content/themes/21-12-2018/img/logo-velox-park.png',
            'distância': '14km',
            'Diária_Vaga_Coberta': response.css("td.col-md-2::text")[0].get(),
            'promoção': response.css("td.col-md-2::text")[1].get()
            }

        
        if response.url =='https://site.bh-airport.com.br/SitePages/pt/estacionamento/index.aspx':

            yield SeleniumRequest(
                url="https://site.bh-airport.com.br/_api/Web/GetList('//Lists/ValoresEstacionamento')/Items", 
                callback=self.parse_result,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.ID, 'spnValorDiariaP'))
                )


        if response.url == "http://www.parkconfins.com.br/":



            yield {
            'nome': 'Park Confins',
            'logo': 'http://www.parkconfins.com.br/wp-content/uploads/2019/03/logo-ParkConfins-Negativo.png',
            'distância': '3,3km',
            'Diária_Coberta': response.css("#et-boc > div > div.et_pb_section.et_pb_section_3.et_section_regular > div > div.et_pb_column.et_pb_column_1_2.et_pb_column_1.et_pb_css_mix_blend_mode_passthrough > div.et_pb_module.et_pb_text.et_pb_text_1.et_pb_bg_layout_light.et_pb_text_align_center > div > div > table > tbody > tr:nth-child(3) > td:nth-child(2)::text")[0].get(),
            'Diária_Descoberta': response.css("#et-boc > div > div.et_pb_section.et_pb_section_3.et_section_regular > div > div.et_pb_column.et_pb_column_1_2.et_pb_column_1.et_pb_css_mix_blend_mode_passthrough > div.et_pb_module.et_pb_text.et_pb_text_1.et_pb_bg_layout_light.et_pb_text_align_center > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2)::text").get(),
            'Semana_Coberta': response.css('#et-boc > div > div.et_pb_section.et_pb_section_3.et_section_regular > div > div.et_pb_column.et_pb_column_1_2.et_pb_column_1.et_pb_css_mix_blend_mode_passthrough > div.et_pb_module.et_pb_text.et_pb_text_1.et_pb_bg_layout_light.et_pb_text_align_center > div > div > table > tbody > tr:nth-child(3) > td:nth-child(3)::text').get(),
            'Semana_Descoberta': response.css('#et-boc > div > div.et_pb_section.et_pb_section_3.et_section_regular > div > div.et_pb_column.et_pb_column_1_2.et_pb_column_1.et_pb_css_mix_blend_mode_passthrough > div.et_pb_module.et_pb_text.et_pb_text_1.et_pb_bg_layout_light.et_pb_text_align_center > div > div > table > tbody > tr:nth-child(2) > td:nth-child(3)::text').get()

            }
            

        if response.url == "http://www.superparkestacionamento.com.br/":



            yield {
            'nome': 'Super Park',
            'logo': 'http://www.superparkestacionamento.com.br/wp-content/themes/superpark/app/images/logo.svg',
            'distância': '6,5km',
            'Coberta': response.css("#precos > div > div:nth-child(2) > div > div > span::text")[0].get(),
            'Semana': response.css("#precos > div > div:nth-child(3) > div > div > span::text")[0].get(),
            'Mensal': response.css('#precos > div > div:nth-child(4) > div > div > span::text')[0].get()
            }


        if response.url == "https://www.estacionamentospacepark.com.br/":



            yield {
            'nome': 'Space Park',
            'logo': 'https://www.estacionamentospacepark.com.br/assets/img/logo.png',
            'distância': '3,6km',
            'Coberta': busca_preco_space(response.css(".lead.mb-5::text")[1].get()),
            'Semana': busca_preco_space(response.css(".lead.mb-5::text")[7].get())
            }


        if response.url == "https://www.centralparkconfins.com.br/tarifas":



            yield {
            'nome': 'Central Park',
            'logo': 'https://static.wixstatic.com/media/f42488_d37ae9a5a0994f4fb7d7bc171320d540~mv2_d_3264_3159_s_4_2.png/v1/crop/x_72,y_358,w_3069,h_2431/fill/w_301,h_236,al_c,q_85,usm_0.66_1.00_0.01/Logo%20Central%20Park.webp',
            'distância': '3,6km',
            'Coberta': busca_preco_space(response.css('#comp-kffu8wbx > h2 > span > span > span > span > span > span::text').get()),
            #'Descoberta': busca_preco_space(response.css("#comp-js694zyj__item-j9sduzlb > h5:nth-child(1) > span > span > span:nth-child(2)::text")[0].get()),
            #'Semana_Coberta': busca_preco_space(response.css("#comp-js694zyj__item-js7xv1yr > h5:nth-child(3) > span:nth-child(1) > span > span::text").get()),
            #'Semana_Descoberta': busca_preco_space(response.css('#comp-js694zyj__item-js7xv1yr > h5:nth-child(2) > span > span > span:nth-child(2)::text').get())
            
            }


        if response.url == 'https://www.estapar.com.br/reserva-de-vaga/horarios?codigo=2203&pid=null&data-entrada='+ hoje + '&data-saida=' + hoje + '&pc=null&parceiro=null':

            
            
            yield SeleniumRequest(
                url="https://www.estapar.com.br/ajax/calendario-preco?codigo=2203&sigla=LGS&area=AP&data_in="+ hoje + "&data_out="+ hoje + "&hora_in=18-00&hora_out=23-59&pc=null", 
                callback=self.parse_result2,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'reserva-info-preco-valor'))
                )
         

        if response.url == "http://www.bpark.com.br/":



            yield {
            'nome': 'Bpark',
            'tarifa': 'suspensão temporária das atividades'
            }



        if response.url == "https://www.parebem.com.br/estacionamento/estacionamento-aeroporto-de-confins/":


            
            yield {
            'nome': 'Pare Bem',
            'logo': 'https://www.parebem.com.br/wp-content/uploads/2020/03/logo-parebem-1.svg',
            'distância': '12,4km',
            'Coberta': response.css('.rich-content table:nth-child(10) tr:nth-child(2) td:nth-child(2)::text').get(),
            'Semana': response.css('.rich-content table:nth-child(10) tr:nth-child(5) td:nth-child(2)::text').get(),
            'Mensal': response.css('.rich-content table:nth-child(10) tr:nth-child(6) td:nth-child(2)::text').get(),
            'promoção': (response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(2) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(3) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(4) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(5) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(6) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(7) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(8) td:nth-child(2)::text").get(),
                         response.css("section:nth-of-type(2) .section-content .rich-content table tbody tr:nth-child(9) td:nth-child(2)::text").get())
       
            }


        if response.url == "http://www.greenlinepark.com.br/":
            pass



            yield {
            'nome': 'Green Line',
            'logo': 'http://www.greenlinepark.com.br/wp-gl/wp-content/themes/11-02-2020/img/logo.svg',
            'distância': '13,5km',
            'tarifa': response.css("body section:nth-child(5) div div:nth-child(2) div:nth-child(1) table tbody tr td::text").get(),
            'promoção': response.css("body section:nth-child(5) div div:nth-child(2) div:nth-child(2) table tbody tr td::text").get(),
                              }


        if response.url == "https://www.autoparkbrasil.com.br/":



            yield {
            'nome': 'Auto Park Brasil',
            'logo': 'https://static.wixstatic.com/media/1be1a2_40ca43d6b3314a77af3aff8def549853~mv2.png/v1/fill/w_171,h_86,al_c,q_85,usm_0.66_1.00_0.01/1be1a2_40ca43d6b3314a77af3aff8def549853~mv2.webp',
            'distância': '4,3km',
            'Diária_Coberta': response.css('#comp-kb13cwxr > h2 > span:nth-child(2) > span > span > span::text').get(),
            'Diária_Descoberta': response.css('#comp-kb13fvtl > h2 > span:nth-child(2) > span > span > span::text').get(),
            'Semana_Coberta': response.css('#comp-kb13encv > h2 > span:nth-child(2) > span > span > span::text').get(),
            'Semana_Descoberta': response.css('#comp-kb13fvvo > h2 > span:nth-child(2) > span > span > span::text').get()

            }

        if response.url == "https://estacionamentopatioconfins.com.br/wp/preco-estacionamento-aeroporto-de-confins/":



            yield {
            'nome': 'Pátio Confins',
            'logo': '/wp/wp-content/uploads/2017/02/logo.png',
            'distância': '3,6km',
            'Diária_Coberta': response.css("body > div.page-builder > div > div > div.col-md-8 > div > blockquote:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(3)::text").get(),
            'Diária_Descoberta': response.css("body > div.page-builder > div > div > div.col-md-8 > div > blockquote:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(2)::text").get(),
            'Semana_Coberta': response.css("body > div.page-builder > div > div > div.col-md-8 > div > blockquote:nth-child(2) > table > tbody > tr:nth-child(8) > td:nth-child(3)::text").get(),
            'Semana_Descoberta': response.css("body > div.page-builder > div > div > div.col-md-8 > div > blockquote:nth-child(2) > table > tbody > tr:nth-child(8) > td:nth-child(2)::text").get()

            }




    def parse_result(self, response):
       # print(response.selector.xpath('//*[@id="spnValorDiariaP"]'))
       response.selector.remove_namespaces()
       yield {
       'nome': 'BH Airport',
       'logo': 'https://site.bh-airport.com.br/SiteAssets/images/logo_bh.png',
       'distância': 'Okm',
       'Premium': response.xpath("//content/properties/ValorDiariaP/text()").get(),
       'Econômico': response.xpath("//content/properties/ValorDiariaE/text()").get(),
       'Motocicletas': response.xpath("//content/properties/ValorDiariaM/text()").get(),
       'Semana': response.xpath("//content/properties/ValorPromoE7Dias/text()").get(),
       }

    def parse_result2(self, response):
        seletor = json.loads(response.text)
        global coberta
        coberta = seletor['price']['reservaveis'][0]['produto']['preco']
        yield SeleniumRequest(
            url="https://www.estapar.com.br/ajax/calendario-preco?codigo=2203&sigla=LGS&area=AP&data_in="+ hoje + "&data_out="+ semana_q_vem + "&hora_in=18-00&hora_out=23-59&pc=null", 
            callback=self.novo_request,
            wait_time=10,
            wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'reserva-info-preco-valor'))
            )
       
       

    def novo_request(self, response):

        seletor = json.loads(response.text)
        
        yield {
       'nome': 'Estapar',
       'logo': 'https://www.estapar.com.br/sites/default/files/logo-estapar-home-nova-estapar.png',
       'distância': '4km',
       'Coberta': coberta,
       'Semana': seletor['price']['reservaveis'][0]['produto']['preco']
       }
        

def busca_preco_space(txt):
    x =str()
    try:
        x = re.findall(r"[0-9]{2}\,[0-9]{2}|[0-9]{3}\,[0-9]{2}", txt)
    
        return x [0]
    except:
        x = re.findall(r"[0-9]{2}\.[0-9]+|[0-9]{3}\.[0-9]{2}", txt)
        
        return x [0]
    