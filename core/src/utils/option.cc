#include <option.h>

template <typename T>
bool utils::Option<T>::isSome() const
{
    return !isNone;
}

template <typename T>
bool utils::Option<T>::isNone() const
{
    return isNone;
}

template <typename T>
T utils::Option<T>::unwrap() const
{
    if (isSome())
    {
        return value;
    }
    else
    {
        throw std::logic_error("Option is None");
    }
}