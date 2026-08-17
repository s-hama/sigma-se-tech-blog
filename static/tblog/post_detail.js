(() => {
  // At 992–1199px, Bootstrap's 960px container leaves 662px for the post body.
  const referencePostBodyWidth = 662;
  const scrollMediaQuery = window.matchMedia('(max-width: 991px)');

  const wrapPostImages = () => {
    document.querySelectorAll('.post-body img').forEach((image) => {
      if (image.closest('.post-media-scroll')) {
        return;
      }

      const postBody = image.closest('.post-body');
      const containingBlockWidth = image.parentElement.clientWidth;
      const nestedHorizontalSpace = Math.max(postBody.clientWidth - containingBlockWidth, 0);
      const referenceContainingBlockWidth = referencePostBodyWidth - nestedHorizontalSpace;
      const scrollContainer = document.createElement('div');
      scrollContainer.className = 'post-media-scroll';
      scrollContainer.dataset.autoScrollContainer = '';
      image.parentNode.insertBefore(scrollContainer, image);
      scrollContainer.appendChild(image);

      const setMediaWidth = () => {
        if (!image.naturalWidth) {
          return;
        }

        const inlineWidthPercent = image.style.width.match(/^(\d+(?:\.\d+)?)%$/);
        const inlineWidthPixels = image.style.width.match(/^(\d+(?:\.\d+)?)px$/);
        const inlineMaxWidthPixels = image.style.maxWidth.match(/^(\d+(?:\.\d+)?)px$/);
        let mediaWidth = image.naturalWidth;

        if (inlineWidthPercent) {
          mediaWidth = referenceContainingBlockWidth * Number(inlineWidthPercent[1]) / 100;
        } else if (inlineWidthPixels) {
          mediaWidth = Number(inlineWidthPixels[1]);
        }

        if (inlineMaxWidthPixels) {
          mediaWidth = Math.min(mediaWidth, Number(inlineMaxWidthPixels[1]));
        }

        mediaWidth = Math.min(mediaWidth, referenceContainingBlockWidth);
        image.style.setProperty('--post-media-width', `${mediaWidth}px`);
      };

      if (image.complete) {
        setMediaWidth();
      } else {
        image.addEventListener('load', setMediaWidth, { once: true });
      }
    });
  };

  const unwrapPostImages = () => {
    document.querySelectorAll('.post-media-scroll[data-auto-scroll-container]').forEach((scrollContainer) => {
      scrollContainer.replaceWith(...scrollContainer.childNodes);
    });
  };

  const updatePostImages = () => {
    if (scrollMediaQuery.matches) {
      wrapPostImages();
    } else {
      unwrapPostImages();
    }
  };

  const initializeSharing = () => {
    const copyButton = document.getElementById('copy-article-url');
    const shareButton = document.getElementById('share-article');
    const status = document.getElementById('share-status');

    if (!copyButton || !shareButton || !status) {
      return;
    }

    const articleUrl = copyButton.dataset.url;
    let statusTimer;

    const showStatus = (message) => {
      window.clearTimeout(statusTimer);
      status.textContent = message;
      statusTimer = window.setTimeout(() => {
        status.textContent = '';
      }, 4000);
    };

    const copyArticleUrl = async () => {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(articleUrl);
        return;
      }

      const textArea = document.createElement('textarea');
      textArea.value = articleUrl;
      textArea.setAttribute('readonly', '');
      textArea.style.position = 'fixed';
      textArea.style.opacity = '0';
      document.body.appendChild(textArea);
      textArea.select();
      const copied = document.execCommand('copy');
      textArea.remove();

      if (!copied) {
        throw new Error('Copy failed');
      }
    };

    copyButton.addEventListener('click', async () => {
      try {
        await copyArticleUrl();
        showStatus('記事のURLをコピーしました。');
      } catch (error) {
        showStatus('URLをコピーできませんでした。');
      }
    });

    if (navigator.share) {
      shareButton.hidden = false;
      shareButton.addEventListener('click', async () => {
        try {
          await navigator.share({
            title: copyButton.dataset.title,
            url: articleUrl,
          });
        } catch (error) {
          if (error.name !== 'AbortError') {
            showStatus('共有メニューを開けませんでした。');
          }
        }
      });
    }
  };

  updatePostImages();
  if (scrollMediaQuery.addEventListener) {
    scrollMediaQuery.addEventListener('change', updatePostImages);
  } else {
    scrollMediaQuery.addListener(updatePostImages);
  }

  initializeSharing();
})();
