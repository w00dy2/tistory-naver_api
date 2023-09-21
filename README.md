# tistory-api와 naver-api를 활용한 핫토픽 top10 자동 포스팅
다음 링크에서 해당 프로젝트가 작성한 글을 볼 수 있다.
https://kwoody01.com/

## 개요
바쁘다고 뉴스를 잘 확인하지 않는 자신을 보며, 그렇다면 매일 어떤 이슈가 있었는지를 기록해놓고 나중에 몰아서라도 볼 수 있으면 좋을 것 같다는 생각에서 코드를 짜게 되었다.

## process
1. 먼저 requests 를 이용한 naver news stand를 크롤링한다.<br>
   crawling()<br>
3. konlpy Hannanum을 이용하여 형태소 분석을 한다.<br>
   countingwords()<br>
4. 분석된 결과를 바탕으로 가장 많이 사용된 단어를 카운트한다. (상위 10개 단어)<br>
   main()<br>
5. naver_api를 사용하여 해당 단어가 포함된 뉴스를 검색한다.<br>
   getNaverSearch()<br>
7. tistory_api를 사용하여 포스팅을 작성한다.<br>
   write_ti()<br>
9. crontab을 사용하여 서버에서 주기적인 위 프로세스를 진행하도록 설정한다.
