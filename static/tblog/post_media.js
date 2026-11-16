(() => {
  // At >= 1400px, Bootstrap's 1320px container leaves 932px for the post body:
  // 1320 * 9/12 - 24px column padding - 32px card padding - 2px card border.
  // Use this same desktop reference even when the page opens on a phone.
  const referencePostBodyWidth = 932;
  // The reference wide figures have ratios of 2.27–2.98. Use 9:4 as the
  // boundary so similarly wide future images receive the same treatment.
  const wideImageAspectRatio = 2.25;
  const scrollMediaQuery = window.matchMedia('(max-width: 991px)');

  const wrapPostImages = () => {
    document.querySelectorAll('.post-body img').forEach((image) => {
      if (image.closest('.post-media-scroll')) {
        return;
      }

      const postBody = image.closest('.post-body');
      let containingBlock = image.parentElement;
      // Inline links/spans do not establish the percentage-width reference.
      while (containingBlock !== postBody && ['inline', 'contents'].includes(getComputedStyle(containingBlock).display)) {
        containingBlock = containingBlock.parentElement;
      }
      const nestedHorizontalSpace = Math.max(
        postBody.clientWidth - containingBlock.clientWidth, 0,
      );
      const referenceWidth = Math.max(referencePostBodyWidth - nestedHorizontalSpace, 1);

      const setMediaWidth = () => {
        // Do not wrap unloaded/broken images; calculate again after loading.
        if (!image.naturalWidth || !image.naturalHeight || !scrollMediaQuery.matches || image.closest('.post-media-scroll')) {
          return;
        }

        const percentWidth = image.style.width.match(/^(\d+(?:\.\d+)?)%$/);
        const pixelWidth = image.style.width.match(/^(\d+(?:\.\d+)?)px$/);
        const maxWidth = image.style.maxWidth.match(/^(\d+(?:\.\d+)?)px$/);
        let desktopWidth = image.naturalWidth;

        if (percentWidth) {
          desktopWidth = referenceWidth * Number(percentWidth[1]) / 100;
        } else if (pixelWidth) {
          desktopWidth = Number(pixelWidth[1]);
        }
        if (maxWidth) {
          desktopWidth = Math.min(desktopWidth, Number(maxWidth[1]));
        }
        desktopWidth = Math.min(desktopWidth, referenceWidth);

        // Resolve the desktop width and cap before applying the CSS scale.
        image.style.setProperty('--post-media-width', `${desktopWidth}px`);

        // A span is valid inside legacy image paragraphs and links as well.
        const scrollContainer = document.createElement('span');
        scrollContainer.className = 'post-media-scroll';
        scrollContainer.dataset.autoScrollContainer = '';
        if (image.naturalWidth / image.naturalHeight >= wideImageAspectRatio) {
          scrollContainer.dataset.wideImage = '';
        }
        // Keep existing image spacing outside the scrollport (including the
        // negative margins in older articles), so the image is not clipped.
        scrollContainer.style.margin = getComputedStyle(image).margin;
        image.before(scrollContainer);
        scrollContainer.appendChild(image);
      };

      if (image.complete) {
        setMediaWidth();
      } else {
        image.addEventListener('load', setMediaWidth, { once: true });
      }
    });
  };

  const unwrapPostImages = () => {
    document.querySelectorAll('.post-media-scroll[data-auto-scroll-container]').forEach((container) => {
      container.querySelectorAll('img').forEach((image) => {
        image.style.removeProperty('--post-media-width');
      });
      container.replaceWith(...container.childNodes);
    });
  };

  const updatePostImages = () => {
    if (scrollMediaQuery.matches) {
      wrapPostImages();
    } else {
      unwrapPostImages();
    }
  };

  updatePostImages();
  scrollMediaQuery.addEventListener('change', updatePostImages);
})();
