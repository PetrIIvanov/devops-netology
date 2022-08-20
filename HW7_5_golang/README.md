<h1>"7.5. Основы golang" - Петр Иванов</h1>

## Задача 1. Установите golang.
1. Воспользуйтесь инструкций с официального сайта: [https://golang.org/](https://golang.org/).
2. Так же для тестирования кода можно использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

## Задача 2. Знакомство с gotour.
У Golang есть обучающая интерактивная консоль [https://tour.golang.org/](https://tour.golang.org/). 
Рекомендуется изучить максимальное количество примеров. В консоли уже написан необходимый код, 
осталось только с ним ознакомиться и поэкспериментировать как написано в инструкции в левой части экрана.  

## Задача 3. Написание кода. 
Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода 
на своем компьютере, либо использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
    Для взаимодействия с пользователем можно использовать функцию `Scanf`:
    ```
    package main
    
    import "fmt"
    
    func main() {
        fmt.Print("Enter a number: ")
        var input float64
        fmt.Scanf("%f", &input)
    
        output := input * 2
    
        fmt.Println(output)    
    }
    ```

## Решение 3.1

Запуск такой
~~~bash
cat data_01.txt | go run task01.go
~~~

Текст

~~~Golang
package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "strconv"
)

func main() {
    // check if there is somethinig to read on STDIN
    stat, _ := os.Stdin.Stat()


    if (stat.Mode() & os.ModeCharDevice) == 0 {
        var stdin []string
        var output string

        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {

            stdin = append(stdin,scanner.Text())

        }

        if err := scanner.Err(); err != nil {
            log.Fatal(err)
        }

        for _, s := range stdin {
            var foots float64
            foots,_ = strconv.ParseFloat(s, 32)
            output = fmt.Sprintf("Meters: %s Foots: %.2f", s, foots * 0.3048)
            fmt.Println(output)
        }
    } else {
        fmt.Println("------------\n\nPlease pass data via stdin\n\n------------\n")
    }
}
~~~ 

 
1. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```
## Решение 3.2

~~~golang
package main

import (
    "fmt"
)

func main() {
    var minimum int
    var x = []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}

    if (len(x) < 1) {
        fmt.Println("Zero length array\n")
    }
    minimum = x[0]

    for _, el := range x {
        if minimum > el {
                minimum = el
        } // end of if
    } // end of for

    fmt.Println(fmt.Sprintf("Minimum is %d", minimum))
}
~~~


1. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.

В виде решения ссылку на код или сам код. 

## Задача 4. Протестировать код (не обязательно).

Создайте тесты для функций из предыдущего задания. 