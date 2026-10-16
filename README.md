# Jihyun Kim Portfolio

Entrepreneur. Creator. Artist. 포트폴리오 웹사이트입니다.

**`index.html` 파일 하나에 디자인(CSS), 애니메이션·WebGL·사운드(JavaScript), 라이브러리(GSAP, ScrollTrigger, Lenis)가 전부 들어 있습니다.**
다른 파일이 따로 필요 없어서, 업로드할 때 폴더가 빠져서 디자인이 깨지는 일이 없습니다.

```
├── index.html     사이트 전체 (이 파일 하나면 동작)
├── images/        작품 이미지
├── tools/sync/    Artifact → GitHub 자동 동기화 도구 (배포에는 포함 안 됨)
└── README.md
```

## Artifact와 실시간 연동

이 저장소는 Claude Artifact **Jihyun Kim Portfolio**(https://claude.ai/artifact/UTC3V9MdeeLvjtouDpZCGn)를 그대로 따라갑니다.

- Artifact에서 **Publish changes**를 누른 뒤, 아래 둘 중 하나를 하면 그때 한 번 동기화가 실행되어 이 저장소의 `index.html`이 새로 만들어지고 push됩니다. 그러면 Vercel이 자동으로 다시 배포합니다.
  - claude.ai의 예약 작업(Scheduled tasks)에서 **Jihyun Kim Portfolio · GitHub에 반영하기**의 **Run** 누르기
  - Claude와의 대화에서 "GitHub에 반영해줘"라고 말하기
- 정해진 시간마다 도는 작업은 없어서, 실행할 때만 비용이 듭니다. (페이지 안의 Publish 버튼은 동기화를 자동으로 깨우지 못합니다. Claude가 Artifact를 게시할 때는 자동으로 반영될 수 있습니다.)
- Edit works에서 올린 작품 이미지도 `images/` 폴더로 함께 옮겨집니다.
- 매번 실제 브라우저로 사이트를 띄워 검사한 뒤에만 push하기 때문에, 깨진 버전은 올라가지 않습니다.
- **수정은 Artifact에서 하세요.** 이 저장소의 `index.html`을 직접 고치면, 다음에 Artifact가 바뀔 때 Artifact 내용으로 덮어써집니다.
- 동기화 절차는 `tools/sync/SYNC.md`에 있습니다.

## Vercel 배포

1. vercel.com → **Add New… → Project** → 이 저장소 **Import**
2. Framework Preset: **Other** / Build Command: 비워두기 / Output Directory: 비워두기
3. **Deploy**. 이후 이 저장소에 변경이 올라갈 때마다 자동으로 다시 배포됩니다.

## 작품(Works) 추가·수정

Artifact의 **Edit works** 버튼으로 추가·수정하면 이 사이트에도 자동으로 반영됩니다(위 연동 참고).
참고로 사이트 안의 목록은 `index.html`에서 `id="works-data"`를 검색하면 나오는 아래 형식입니다.

```json
{"v":1,"items":[
  {"id":"w1","cat":"screenplays","title":"작품 제목","year":"2025","role":"Writer","desc":"한 줄 설명","link":"https://...","image":""}
]}
```

- `cat`(분야): `websites`, `screenplays`, `webtoons`, `films`, `shortform`, `awards` 중 하나
- `link`, `image`는 비워둬도 됩니다(`""`). 이미지가 없으면 분야별 실크 질감 이미지가 자동으로 나옵니다.
- `image`: `https://`로 시작하는 이미지 주소, 또는 `images/` 폴더에 넣은 파일 경로(예: `images/poster.jpg`)
- 쉼표·따옴표 형식(JSON)이 틀리면 목록이 비어 보이니 주의하세요.

## 참고

- **음악·효과음**: 음원 파일 없이 브라우저(Web Audio)에서 실시간으로 만들어집니다. 브라우저 정책상 방문자가 처음 클릭/터치할 때 소리가 시작되고, 왼쪽 아래 Sound 버튼으로 켜고 끕니다.
- **폰트**: Google Fonts(Bodoni Moda, Cormorant Garamond)에서 불러옵니다.
- **Edit works 편집 패널**은 Claude Artifact 전용 기능이라 배포된 사이트에는 버튼이 보이지 않습니다. 작품은 Artifact에서 수정하면 자동으로 반영됩니다.
