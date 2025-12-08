function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';

        for (let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');


            tdTitleRus.innerText = films[i].title_ru;

            // оригинальное в скобках, курсивом, если отличается от русского
            if (films[i].title !== films[i].title_ru) {
                tdTitle.innerHTML = `<i>(${films[i].title})</i>`;
            } else {
                tdTitle.innerHTML = '';
            }
            tdYear.innerText = films[i].year;


            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.classList.add('edit-btn');
            editButton.onclick = function () {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.classList.add('delete-btn');
            delButton.onclick = function () {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    });
}



function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}/`, { method: 'DELETE' })
        .then(function () {
            fillFilmList();
        });
}



function showModal() {
    document.getElementById('modal').style.display = 'block';

    // очистка ошибок
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
}



function hideModal() {
    document.getElementById('modal').style.display = 'none';
}



function cancel() {
    hideModal();
}



function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    showModal();
}



function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = id === '' 
        ? '/lab7/rest-api/films/'          // правильный URL для POST
        : `/lab7/rest-api/films/${id}/`;   // правильный URL для PUT

    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(function(resp) {

        if (resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }

        return resp.json();
    })
    .then(function(errors) {

        if (!errors) return;

        if (errors.title)
            document.getElementById('title-error').innerText = errors.title;

        if (errors.title_ru)
            document.getElementById('title-ru-error').innerText = errors.title_ru;

        if (errors.year)
            document.getElementById('year-error').innerText = errors.year;

        if (errors.description)
            document.getElementById('description-error').innerText = errors.description;
    });

}



function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}/`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {

            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;

            showModal();
        });
}
