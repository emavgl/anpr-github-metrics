FROM golang:1.8.4-alpine3.6
MAINTAINER https://github.com/damdo
RUN apk update; apk add --no-cache git nodejs-npm

ENV HTTP_PORT 4000
ENV PUBLIC_DIR public
WORKDIR /go/src/app/
ADD main.go /go/src/app/main.go
RUN go-wrapper download; go-wrapper install
RUN go build -o /go/src/app/main /go/src/app/main.go

ADD ./public /go/src/app/public
RUN cd public/; npm install;
EXPOSE 4000
CMD ["/go/src/app/main"]
