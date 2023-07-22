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
  const horizon = lineController.value;

  const data = {
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
        // horizon: Number(horizon)
      },
      ocr_config: {
        input_path: output_path,
        use_gpu,
        thread_count: Number(thread_count)
      }
    }
  };

  console.log(data);
  return data;
}

function search_books(index) {
  const books = document.querySelectorAll('.book');
  books.forEach(book => {
    book.classList.remove('searched');
  });

  index.forEach(i => {
    if (i < books.length) {
      books[i].classList.add('searched');
    }
  });
}

function add_books(books) {
  const bookshelf = document.querySelectorAll('.bookshelf')[0];

  bookshelf.childNodes.forEach(child => bookshelf.removeChild(child));

  books.forEach(book => {
    var newDiv = document.createElement('div');
    newDiv.className = 'book';

    var newParagraph = document.createElement('p');
    var textNode = document.createTextNode(book);
    newParagraph.appendChild(textNode);
    newDiv.appendChild(newParagraph);

    bookshelf.appendChild(newDiv);
  });
}

const loader = document.querySelector('#state');

function startLoadingAnimation() {
  loader.style.display = 'block';
}

function stopLoadingAnimation() {
  loader.style.display = 'none';
}

function update() {
  startLoadingAnimation();
  $.ajax({
    type: "GET",
    url: "/update",
    success: function (response) {
      add_books(response.books);
      stopLoadingAnimation();
    },
    error: function(xhr, status, error) {
      console.error(error);
      stopLoadingAnimation();
      alert(error);
    }
  });
}

const navItems = document.querySelectorAll('.nav-item');
const pages = document.querySelectorAll('.page');
const save = document.querySelector('.save');
const update_button = document.querySelector('.update');
const search = document.querySelector('.search');
const asr = document.querySelector('.asr');

update_button.addEventListener('click', update);

save.addEventListener('click', () => {
  const config = get_config();
  $.ajax({
        type: "POST",
        url: "/config",
        data: JSON.stringify(config),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
          console.log(response);
          alert(`${response.message}`);
        },
        error: function(xhr, status, error) {
          console.error(error);
          alert(error);
        }
    });
});

search.addEventListener('click', () => {
  startLoadingAnimation();
  const data = {
    description: document.getElementById('search').value
  };
  $.ajax({
        type: "POST",
        url: "/query",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
          const data = response.result;
          search_books(data);
          stopLoadingAnimation();
        },
        error: function(xhr, status, error) {
          console.error(error);
          stopLoadingAnimation();
          alert(error);
        }
  });
});

asr.addEventListener('click', () => {
  startLoadingAnimation();
  $.ajax({
        type: "GET",
        url: "/record",
        success: function (response) {
          const data = response.result;
          search_books(data);
          stopLoadingAnimation();
        },
        error: function(xhr, status, error) {
          console.error(error);
          stopLoadingAnimation();
          alert(error);
        }
  });
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

const horizonLine = document.querySelector('.horizon-line');
const lineController = document.getElementById('horizon');

function getHeight()
{
  let value = lineController.value;
  const height = image.height;
  horizonLine.style.bottom = `${height * (100 - value) / 100}px`;
}

lineController.addEventListener('input', getHeight);

update();
getHeight();