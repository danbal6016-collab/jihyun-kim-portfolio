# Jihyun Kim Portfolio

Entrepreneur. Creator. Artist. 포트폴리오 웹사이트입니다.

**`index.html` 파일 하나에 디자인(CSS), 애니메이션·WebGL·사운드(JavaScript), 라이브러리(GSAP, ScrollTrigger, Lenis)가 전부 들어 있습니다.**
다른 파일이 따로 필요 없어서, 업로드할 때 폴더가 빠져서 디자인이 깨지는 일이 없습니다.

```
├── index.html     사이트 전체 (이 파일 하나면 동작)
├── images/        작품 이미지를 넣고 싶을 때 쓰는 폴더 (선택)
└── README.md
```

## Vercel 배포

1. vercel.com → **Add New… → Project** → 이 저장소 **Import**
2. Framework Preset: **Other** / Build Command: 비워두기 / Output Directory: 비워두기
3. **Deploy**. 이후 이 저장소에 변경이 올라갈 때마다 자동으로 다시 배포됩니다.

## 작품(Works) 추가·수정

`index.html`에서 `id="works-data"`를 검색하면 나오는 목록을 고칩니다.

```json
{"v":1,"items":[
  {"id":"w1","cat":"screenplays","title":"작품 제목","year":"2025","role":"Writer","desc":"한 줄 설명","link":"https://...","image":""}
]}
```

- `cat`(분야): `websites`, `screenplays`, `webtoons`, `films`, `awards` 중 하나
- `link`, `image`는 비워둬도 됩니다(`""`). 이미지가 없으면 분야별 실크 질감 이미지가 자동으로 나옵니다.
- `image`: `https://`로 시작하는 이미지 주소, 또는 `images/` 폴더에 넣은 파일 경로(예: `images/poster.jpg`)
- 쉼표·따옴표 형식(JSON)이 틀리면 목록이 비어 보이니 주의하세요.

## 참고

- **음악·효과음**: 음원 파일 없이 브라우저(Web Audio)에서 실시간으로 만들어집니다. 브라우저 정책상 방문자가 처음 클릭/터치할 때 소리가 시작되고, 왼쪽 아래 Sound 버튼으로 켜고 끕니다.
- **폰트**: Google Fonts(Bodoni Moda, Cormorant Garamond)에서 불러옵니다.
- **Edit works 편집 패널**은 Claude Artifact 전용 기능이라 이 사이트에는 없습니다. 작품은 위 방법으로 수정하세요.
