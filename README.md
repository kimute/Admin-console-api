# SP management console API

## Description

API for User Authenication & create JSON file for single Tenant APP Build
(with AWS cognito and Lambda)


## Environments

| container name | environment  | remarks |
| -------------- | ------------ | ------- |
| fast_api       | pyhton 3.9.0 | fastApi |

## How to build 　(local)

1. create folder`src/.env`

   refer to sample`.evv.sample`

2. Launch Docker container with the following command

   ```console
   docker-compose up -d
   ```

3. how to access API

   `http://0.0.0.0:8000/docs`

4. Docker container close
   ```console
   docker-compose down
   ```

## environmental variable |

| variable name | 内容       | ex            |
| ------------- | ---------- | ------------- |
| DB_USER_NAME  | DB user ID | 'user'        |
| DB_USER_PASS  | DB pass    | 'user passwd' |
| DB_HOST       | DB HOST 名 | 'localhost'   |
| DB_PORT       | host       | 3308          |
| DB_NAME       | DB schema  | 'test_user'   |

## reference

- dockerfile is under `docker/bacend/`
- Add required applications to`requirements.txt`
- Sql files in `docker/mysql/initdb.d` run during initial database build

## set up mysql in local PC

- docker-compose up -d 後　 docker-compose exec db bash -c 'mysql -u root -p'で mysql 　 user 設定をする,password は env で設定した password →
- → GRANT ALL PRIVILEGES ON _._ to 'user'@'%' identified by "password";
- → 　 flush privileges;
