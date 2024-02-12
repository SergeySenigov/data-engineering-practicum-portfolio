# data-engineer-practicum-portfolio
Проекты специализации Data Engineer, созданные в ходе курса Yandex Practicum  

| Проект              | Цели проекта           | Используемые технологии, библиотеки, инструменты| Навыки |
| :-------------------- | :--------------------- |:---------------------------|:---------------------------|
| [Data Cleansing, User Retention DataMart](</1 Data Cleansing, User Retention DataMart Creation/README.md>)         | Проверить качество исходных данных (пропуски, повторы, форматы, некорректные записи)   <P><P>Создать витрины данных для RFM-классификации пользователей           | SQL, CTE, Window Functions, PostgreSQL, cloudbeaver | Расширил навыки использования оконных функций, встроенных в `PostgreSQL` механизмов проверок данных <P><P>Научился использовать `Common Table Expression`, познакомился с инструментом `cloudbeaver`
| [DataModel Review, Migration To A New Model](</2 DWH, DataModel Review, Migration to New Model/README.md>) | Мигрировать данные в отдельные логические таблицы  <P><P>Создать витрину данных для новой модели данных   | SQL, Window Functions, PostgreSQL, cloudbeaver          | Изучил принципы построения `DataWareHouse` <P><P> Изучил состав и назначение слоев хранилища данных
| [DataMart Review, Idempotence Support](</3 ETL Update, DataMart Review, Idempotence/README.md>)         | Модифицировать процессы в пайплайне, чтобы они соответствовали новым задачам бизнеса, обеспечив обратную совместимость <P><P>Создать обновленную витрину данных для исследования возвращаемости клиентов<P><P>Модифицировать ETL процесс, чтобы поддерживалась идемпотентность         | AirFlow, SQL, PostgreSQL, cloudbeaver, bash, pandas, SQLAlchemy      | Изучил принципы реализации оркестрации, реализовал оркестрацию с помощью `Airflow` <P><P>Научился работать с `PostgreSQL` из Python с помощью библиотек `psycopg2`, `SQLAlchemy` <P><P>Изучил подход к реализации идемпотентности. 
| [Data Quality Checks](</4 Check Data Quality, Check Pipeline/README.md>)     | Определить, на каких этапах ETL процесса внедрить проверки качества данных <P><P>Разработать и внедрить проверки в ETL процесс <P><P>Создать  витрину данных с результатами проверок <P><P>Составить инструкции по поддержке процессов с проверками          | AirFlow, SQL, PostgreSQL         | Расширил навыки работы с `Airflow` <P><P> Получил навыки работы с файлами средствами `Python` <P><P> Научился писать `RunBook` для администраторов
| [Multiple Data Sources, Analytical DataMart](</5 DWH With Multiple Sources, DataMart Creation/README.md>)        | Усовершенствовать хранилище данных: добавить новый источник и витрину <P><P>Связать данные из нового источника с данными в хранилище <P><P>Реализовать витрину для расчётов с курьерами           | Airflow, PostgreSQL, MongoDB Compass, pendulum, Jupyter Notebook, bash, SQLAlchemy    | На практике получил навык работы с БД типа `NoSQL` <P><P>Упрочил навыки реализации пайпланов в `Airflow` <P><P>Расширил навыки работы с пакетом `requests`
| [Analytical DataBases](</6 Analytical DataBases, Vertica, DataMart Creation/README.md>)         | Расширить модель данных в аналитической БД<P><P>Разработать витрину данных для оценки эффективности рекламы          | AirFlow, Yandex S3 Storage, Common Table Expression, SQL, Vertica, cloudbeaver, pandas         |
| [Data Lake With Hadoop, HDFS](</7 Spark, Data Lake with Hadoop, HDFS/README.md>)       | Расширить структуру данных в Data Lake <P><P>Создать четыре витрины данных в HDFS, автоматизировать их обновление        | PySpark, SQL, Window Functions, Hadoop, HDFS, Airflow, Jupyter Notebook
| [Data Stream Processing](</8 Data Stream Processing>)         | Создать сервис потоковой обработки данных, расширяющий возможности онлайн приложения по доставке еды: обогащение входной информации данными из БД, отправка сообщений в выходной поток          | Kafka, PySpark, AirFlow, kcat, Jupyter Notebook, SQL, PostgreSQL, Spark Streaming          |
| [Yandex Cloud Services](<9 Yandex Cloud Services>)        | Создать на платформе Yandex Cloud три сервиса, которые реализуют ETL процесс <P><P>Визуализировать данные из новой витрины в дашборде в Datalense          | Yandex Cloud Services, Datalense, Kubernetes, kubectl, Kafka, kcat, confluent_kafka, flask, docker, Redis         |
| [Fintech Data Processing, Analytical Datamart](</10 Fintech Data Processing, Analytic Datamart>)         | Для финтех-компании, предлагающей международные банковские услуги, объединить из разных источников информацию о финансовой активность пользователей  <P><P>Подготовить информацию для аналитики в дашборде           | Yandex S3 Storage, Metabase, Vertica, vertica_python, boto3, Airflow       |
---  
