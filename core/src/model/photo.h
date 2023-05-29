#ifndef PHOTO_H
#define PHOTO_H

#include <vector>
#include <option.h>

namespace model
{
    enum class PhotoType
    {
        GRAY,
        RGB
    };

    class Photo
    {
    public:
        Photo();
        explicit Photo(PhotoType type);
        Photo(PhotoType type, const std::vector<unsigned char> &data);
        ~Photo();

        void set_type(PhotoType type);
        utils::Option<PhotoType> get_type() const;

        void set_data(const std::vector<unsigned char> &data);
        utils::Option<std::vector<unsigned char>> get_data() const;

    private:
        utils::Option<PhotoType> type;
        utils::Option<std::vector<unsigned char>> data;
    };
}

#endif