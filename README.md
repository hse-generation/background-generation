# Genme
[Онлайн-сервис](https://genme.ru/) для создания и редактирования инфографики для маркетплейсов (Ozon, Wildberries).

Для разработки этого проекта использовался Django - фреймворк Python для создания веб-приложений. HTML, CSS и JS использовались для создания пользовательского интерфейса сайта. Django предоставляет различные инструменты для работы с базой данных, управления аутентификацией пользователей и разработки веб-приложений.


Связь с маркетплйсами, а также с моделями для удаления/генерации фона реализована с помощью API.

# Личный кабинет
После регистрации пользователю предлагается заполнить некоторую информацию, а именно:  
* имя;
* client id (ozon);
* api key (ozon);
* api key (WB);
* фотография профиля.

После ввода ключей для маркетплейсов у пользователя появляются страницы для работы с ними.

Из личного кабинета пользователь может удалить свой аккаунт, что повлечет удаление его из базы данных сайта.

# Страница магазина
Здесь отображаются товары (название и фотография-обложка) с текущего маркетплейса. Также здесь показывается рейтинг товара, выставленный самим магазином, для определения товаров, которые нуждаются в доработке. Также отсюда можно перейти на страницу выбора фотографии для редактирования.

# Страница товара
Здесь показываются все фотографии товара, его полное описание и название. На этой странице происходит выбор изображения для редактирования, либо загрузка нового изображения.

# Редактирование
Здесь отображается выбранная фотография до редактирования и после него, а также расположен следующий функционал:
* отразить изображение по горизонтали;
* удалить фон с возможностью генерации нового по текстовому запросу;
* добавить текст на изображение с возможностью выбора размера текста, его расположения, цвета и шрифта.

После завершения редактирования результат можно либо скачать, либо сразу отправить на платформу.

# Результат
Пользователь получает необходимый функционал для продвинутой настройки инфографики своих товаров и возможность отправки изменений сразу на маркетплейсы.
