# Stage 1: Build the Go application
FROM golang:latest AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Create a minimal image to run the Go app
FROM alpine:latest  

WORKDIR /app

COPY --from=builder /app/main .

EXPOSE 8080

CMD ["/app/main"]
