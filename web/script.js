function updateImage() {
  const points = get_angle_points();
  const [x1, y1] = points[0];
  const [x3, y3] = points[1];
  const [x4, y4] = points[2];
  const [x2, y2] = points[3];

  image.style.clipPath = `polygon(${x4}% ${y4}%, ${x3}% ${y3}%, ${x1}% ${y1}%, ${x2}% ${y2}%)`;
}

function get_angle_points() {
  const x1 = document.getElementById('left-top-x').value;
  const y1 = document.getElementById('left-top-y').value;
  const x2 = document.getElementById('left-bottom-x').value;
  const y2 = document.getElementById('left-bottom-y').value;
  const x3 = document.getElementById('right-top-x').value;
  const y3 = document.getElementById('right-top-y').value;
  const x4 = document.getElementById('right-bottom-x').value;
  const y4 = document.getElementById('right-bottom-y').value;

  return [[Number(x1), Number(y1)], [Number(x3), Number(y3)], [Number(x4), Number(y4)], [Number(x2), Number(y2)]];
}

function get_config() {
  const host = document.getElementById('host').value;
  const input_path = document.getElementById('input_path').value;
  const output_path = document.getElementById('output_path').value;
  const scale = document.getElementById('scale').value;
  const eps = document.getElementById('eps').value;
  const min_height_rate = document.getElementById('min_height_rate').value;
  const count = document.getElementById('count').value;
  const use_gpu = document.getElementById('use_gpu').checked;
  const thread_count = document.getElementById('thread_count').value;

  return {
    host,
    config: {
      segment_config: {
        input_path,
        output_path,
        angle_point: get_angle_points(),
        img_scale: Number(scale),
        min_height_rate: Number(min_height_rate),
        eps: Number(eps),
        count: Number(count)
      },
      ocr_config: {
        input_path: output_path,
        use_gpu,
        thread_count: Number(thread_count)
      }
    }
  };
}

function set_other_config() {
  // TODO: 设置其他配置
}

function search_book(index) {
  const books = document.querySelectorAll('.book');
  books.forEach(book => {
    book.classList.remove('searched');
  });

  index.forEach(i => {
    books[i].classList.add('searched');
  });
}

const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const save = document.querySelector('.save');

save.addEventListener('click', () => {
  const config = get_config();
  console.log(config);
  // TODO: 在面板上保存配置
});

pages.forEach(page => {
  page.style.display = 'none';
});
pages[0].style.display = 'block';
navItems[0].classList.add('selected');

navItems.forEach(navItem => {
  navItem.addEventListener('click', () => {
    const navItemId = navItem.getAttribute('id');

    pages.forEach(page => {
      page.style.display = 'none';
    });

    pages.forEach(page => {
      if (page.id === navItemId) {
        page.style.display = 'block';
      }
    });

    navItems.forEach(item => {
      item.classList.remove('selected');
    });

    navItem.classList.add('selected');
  });
});

const image = document.getElementById('image');
const sliders = document.querySelectorAll('.slider');

sliders.forEach(slider => {
  slider.addEventListener('input', updateImage);
});

const lineContainers = document.querySelectorAll('.line-container');

lineContainers.forEach(container => {
  const h4 = container.querySelector('.value');
  const input = container.querySelector('input');

  if (h4) {
    h4.textContent = input.value;

    input.addEventListener('input', () => {
      h4.textContent = input.value;
    });
  }
});

search_book([2]);
