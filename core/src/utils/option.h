#ifndef OPTION_H
#define OPTION_H

namespace utils
{
    template <typename T>
    class Option
    {
    private:
        bool isNone;
        T value;

    public:
        Option() : isNone(true), value(){};
        Option(const T &value) : isNone(false), value(value){};

        bool isSome() const;

        bool isNone() const;

        T unwrap() const;
    };
}

#endif