import requests
import json
from database import SessionLocal, engine
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table, insert, MetaData, select
import logging
from datetime import datetime, timezone, timedelta

router = APIRouter(
    prefix='/db'
)
with open("./static/AUTH_KEY.json", "r") as json_file:
    cred = json.load(json_file)
    
API_BASE = cred['API_BASE']
AUTH_KEY = cred['AUTH_KEY']

#####################################################################################################################
#
# CMS 게시판 목록에 API 요청
# API_ENDPOINT = 'https://api.cnu.ac.kr/svc/offcam/pub/cmsBoard?AUTH_KEY=AUTH_KEY'
# request_params = {}
# response json 
# OutBlock [
#     {
#        'MSG': success (511)
#     }
# ]
# RESULT [
#     {
#       'site_nm': '정보화본부'
#       'board_no': 87,
#       'board_nm': '충남대학교 정보화본부공지사항'
#     },
#     {
#       'site_nm': '정보화본부'
#       'board_no': 87,
#       'board_nm': '충남대학교 정보화본부공지사항'
#     }, ...    
# ]
#
#  method:
#  - get_site_nm_dict() : site_nm에 학과 고유 번호를 부여하여 json으로 저장 가끔 실행하거나, 실행하지 않음
#  - get_cmsBoard(): cmsBoard 요청을 보내 response를 DB에 저장
#
#####################################################################################################################
@router.get("/get_site_nm_dict")
def get_site_nm_dict():
    params = {"AUTH_KEY": AUTH_KEY}
    try:
        response = requests.get(f"{API_BASE}/cmsBoard", params=params)
    except Exception as e:
        raise print("예외가 발생했습니다.", e)

    response = response.json()
    status = response['OutBlock']
    result = response['RESULT'] 

    site_nm_list = []
    site_nm_dict = {}
    for item in result:
        site_nm = item['site_nm']        
        site_nm_list.append(site_nm)
        
    site_nm_list = sorted(set(site_nm_list)) # 중복 제거, 오름차순 정렬 후, index로 고유번호부여

    for idx, site_nm in enumerate(site_nm_list):
        site_nm_dict[site_nm] = idx #

    with open('./static/site_nm.json', 'w') as f:
        json.dump(site_nm_dict, f, ensure_ascii=False, indent=4)
        
@router.get("/get_cmsBoard")
def get_cmsBoard():
    _session = SessionLocal()
    metadata_obj = MetaData(bind=engine)
    board_table = Table("boards", metadata_obj, autoload_with=engine)
    with open ('./static/site_nm.json', 'r') as f:
        site_nm_dict = json.load(f)
        
    params = {"AUTH_KEY": AUTH_KEY}
    try:
        response = requests.get(f"{API_BASE}/cmsBoard", params=params)
    except Exception as e:
        raise print("예외가 발생했습니다.", e)

    response = response.json()
    status = response['OutBlock']
    result = response['RESULT'] 

    for item in result:
        site_nm = item['site_nm']
        site_no = site_nm_dict[site_nm]
        board_no = item['board_no']        
        board_nm = item['board_nm']
        
        try:
            stmt = insert(board_table).values(site_name=site_nm, department_id = site_no, board_id = board_no, board_name = board_nm) # 명시를 해야 돌아감
            _session.execute(stmt)
            _session.commit()
            # _session.execute(f'Insert Into mmgg.boards values ()')
        except IntegrityError as e:
            message = e.args[0]
            if "Duplicate entry" in message:
                logging.info("Error while executing %s.\n%s.", e.statement, message)
                
#####################################################################################################################
#
# CMS 게시판 내용에 API 요청
# API_ENDPOINT = 'https://api.cnu.ac.kr/svc/offcam/pub/homepageboardContents?P_board_no=P_board_no&AUTH_KEY=AUTH_KEY'
# request params
# 
# response json 
# {
#   P_board_no: board_id   
# }   
# OutBlock [
#     {
#        'MSG': success (511) # 총 갯수
#     }
# ]
# RESULT [
# {
#     "board_no": 87,
#     "article_no": 326632,
#     "article_title": "2023년 정보보호교육센터 교육안내",
#     "article_text": "<div class=\"fr-view\"><p><img src=\"https://cic.cnu.ac.kr/_res/cic/img/2023정보보호교육안내001.png\" style=\"max-width: 100%; height: auto;\" class=\"fr-fic fr-dii\"></p><p><a href=\"https://sec.keris.or.kr\" target=\"_new\"><img class=\"fr-fic fr-dii\" style=\"height: auto; max-width: 100%;\" src=\"https://cic.cnu.ac.kr/_res/cic/img/2023정보보호교육안내002.png\"></a></p><p><img src=\"https://cic.cnu.ac.kr/_res/cic/img/2023정보보호교육안내_003.png\" style=\"max-width: 100%; height: auto;\" class=\"fr-fic fr-dii\"></p><p><img src=\"https://cic.cnu.ac.kr/_res/cic/img/2023정보보호교육안내_004.png\" style=\"max-width: 100%; height: auto;\" class=\"fr-fic fr-dii\"></p><p><img src=\"https://cic.cnu.ac.kr/_res/cic/img/2023정보보호교육안내005.png\" style=\"max-width: 100%; height: auto;\" class=\"fr-fic fr-dii\"></p></div>",
#     "writer_nm": "정보화본부",
#     "click_cnt": 98,
#     "attach_cnt": 0,
#     "update_dt": {
#         "date": 4,
#         "day": 2,
#         "hours": 14,
#         "minutes": 50,
#         "month": 3,
#         "nanos": 0,
#         "seconds": 20,
#         "time": 1680587420000,
#         "timezoneOffset": -540,
#         "year": 123
#     }
# },
# {
#     "board_no": 87,
#     "article_no": 326313,
#     "article_title": "충남대학교 학내 정보시스템(포탈, 지능형 통합정보시스템, 모바일 등) 개선을 위한 설문조사 참여 요청",
#     "article_text": "<div class=\"fr-view\"><p>우리 정보화본부에서는 포탈 시스템, 지능형 통합정보시스템, 모바일 등 학생 및 교수의 불편사항과 기능개선 요구사항을&nbsp;</p><p><br></p><p>검토‧반영하기 위해 아래와 같이 설문을 실시하오니, &nbsp;</p><p><br></p><p>많은 참여 부탁드리겠습니다.&nbsp;</p><p><br></p><p><br></p><p>1. 참여대상 : 학생 및 교수 ※ 직원은 지능형 통합정보시스템 정보화서비스 요청(ITSM)에서 상시적으로 요구사항 접수&nbsp;</p><p><br></p><p>2. 조사기간 : 2023. 3. 31.(금) ~ 4. 14.(금)&nbsp;</p><p><br></p><p>3. 조사내용 : 학생 및 교수 불편사항 및 기능개선 요구사항 수집</p><p><br></p><p>4. 설문조사 URL &nbsp;</p><p><br></p><p><br></p><p><br></p><table style=\"width: 61%; margin-right: calc(39%);\"><tbody><tr><td style=\"width: 10.5725%; height: 17.65pt; padding: 1.41pt 5.1pt; background: rgb(231, 244, 246); vertical-align: middle;\" valign=\"middle\"><p style=\"text-align:center;\"><span style=\"font-family:굴림체;font-weight:bold;font-size:16px;\">구분</span></p></td><td colspan=\"2\" style=\"width: 89.3387%; height: 17.65pt; padding: 1.41pt 5.1pt; background: rgb(231, 244, 246); vertical-align: middle;\" valign=\"middle\"><p style=\"text-align:center;\"><span style=\"font-family:굴림체;font-weight:bold;font-size:16px;\">설문조사&nbsp;</span><span style=\"font-family:굴림체;font-weight:bold;font-size:16px;\">URL</span></p></td></tr><tr><td style=\"width: 10.5725%; height: 28.61pt; padding: 1.41pt 5.1pt; vertical-align: middle; text-align: center;\" valign=\"middle\"><p style=\"margin-right:5.0pt;text-align:center;\"><span style=\"font-family:굴림체;font-weight:bold;\">학생&nbsp;</span></p></td><td style=\"width: 30.1913%; height: 28.61pt; padding: 1.41pt 5.1pt; vertical-align: middle;\" valign=\"middle\"><p style=\"margin-right:5.0pt;font-weight:bold;\"><a href=\"http://tmurl.kr/7i0x\"><u><span style=\"font-family:굴림체;font-weight:bold;color:#0000ff;\">http://tmurl.kr/7i0x</span></u></a></p></td><td style=\"width: 59.0982%; height: 28.61pt; padding: 1.41pt 5.1pt; vertical-align: middle;\" valign=\"middle\"><p style=\"margin-right:5.0pt;text-align:center;font-weight:bold;\"><img src=\"/_attach/image/editor_image/2023/03/ZGTNIhOzUiOpqrVEIQla0.jpg\" class=\"fr-fic fr-dib\" data-path=\"/_attach/image/editor_image/2023/03/ZGTNIhOzUiOpqrVEIQla0.jpg\" data-size=\"7489\" data-success=\"true\" data-file_name=\"ZGTNIhOzUiOpqrVEIQla0.jpg\" data-alt=\"screen shot\"></p></td></tr><tr><td style=\"width: 10.5725%; height: 34.27pt; padding: 1.41pt 5.1pt; vertical-align: middle; text-align: center;\" valign=\"middle\"><p style=\"margin-right:5.0pt;text-align:center;\"><span style=\"font-family:굴림체;font-weight:bold;\">교수</span></p></td><td style=\"width: 30.1913%; height: 34.27pt; padding: 1.41pt 5.1pt; vertical-align: middle;\" valign=\"middle\"><p style=\"margin-right:5.0pt;font-weight:bold;\"><a href=\"http://tmurl.kr/7i0w\"><u><span style=\"font-family:굴림체;font-weight:bold;color:#0000ff;\">http://tmurl.kr/7i0w</span></u></a></p></td><td style=\"width: 59.0982%; height: 34.27pt; padding: 1.41pt 5.1pt; vertical-align: middle;\" valign=\"middle\"><p style=\"margin-right:5.0pt;text-align:center;font-weight:bold;\"><img src=\"/_attach/image/editor_image/2023/03/RDkOTSdmgaIjUqKFxqDJ0.jpg\" class=\"fr-fic fr-dib\" data-path=\"/_attach/image/editor_image/2023/03/RDkOTSdmgaIjUqKFxqDJ0.jpg\" data-size=\"7298\" data-success=\"true\" data-file_name=\"RDkOTSdmgaIjUqKFxqDJ0.jpg\" data-alt=\"screen shot\"></p></td></tr></tbody></table><p><br></p><p><br></p></div>",
#     "writer_nm": "정보화본부",
#     "click_cnt": 178,
#     "attach_cnt": 0,
#     "update_dt": {
#         "date": 3,
#         "day": 1,
#         "hours": 9,
#         "minutes": 29,
#         "month": 3,
#         "nanos": 0,
#         "seconds": 48,
#         "time": 1680481788000,
#         "timezoneOffset": -540,
#         "year": 123
#     }
# },   
# ]
#
#  method:
#  - get_homepageBoardContents(): homepageboardContents 요청을 보내 response를 DB에 저장
#####################################################################################################################

@router.get("/get_homepageBoardContents")
def get_homepageBoardContents():
    _session = SessionLocal()
    metadata_obj = MetaData(bind=engine)
    board_table = Table("boards", metadata_obj, autoload_with=engine)
    content_table = Table("contents", metadata_obj, autoload_with=engine)
    with open ('./static/site_nm.json', 'r') as f:
        site_nm_dict = json.load(f)
        
    board_ids = _session.execute(select(board_table.c.board_id)).all()
    board_ids = [i[0] for i in board_ids]
    # print(board_ids)
    
    # get response
    for P_board_no in board_ids[:30]:
        if P_board_no is None:
            continue
        params = {"P_board_no": P_board_no,"AUTH_KEY": AUTH_KEY}
        try:
            response = requests.get(f"{API_BASE}/homepageboardContents", params=params)
        except Exception as e:
            raise print("예외가 발생했습니다.", e)
        try:
            response = response.json()
        except:
            continue
        status = response['OutBlock']
        result = response['RESULT']
        _department_id = _session.execute(select(board_table.c.department_id)
                                         .where(board_table.c.board_id == P_board_no)).all()[0][0]
        # print(_department_id)
        for item in result:
            board_no = item['board_no']
            article_no = item['article_no']
            department_id = _department_id
            article_title = item['article_title']
            article_text = item['article_text']
            click_cnt = item['click_cnt']
            writer_name = item['writer_nm']
            attach_cnt = item['attach_cnt']
            update_dt = datetime.utcfromtimestamp(item['update_dt']['time']/ 1000.0) + timedelta(hours=9)
        
            try:
                stmt = insert(content_table)\
                       .values(content_id=article_no, 
                               board_id = board_no, 
                               department_id = department_id,
                               title = article_title,
                               body = article_text,
                               writer_name = writer_name,
                               click_cnt = click_cnt,
                               attach_cnt = attach_cnt,
                               update = update_dt) # 명시를 해야 돌아감
                _session.execute(stmt)
                _session.commit()
                # _session.execute(f'Insert Into mmgg.boards values ()')
            except IntegrityError as e:
                message = e.args[0]
                if "Duplicate entry" in message:
                    logging.info("Error while executing %s.\n%s.", e.statement, message)
                    
        print(f'Board : {board_no}의 items {len(result)}가 성공적으로 삽입되었습니다.')

if __name__ == "__main__":
    # get_site_nm_dict()
    get_cmsBoard()