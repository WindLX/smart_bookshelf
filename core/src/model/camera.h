#ifndef CAMERA_H
#define CAMERA_H

#include <photo.h>

namespace model
{
    class ICamera
    {
    public:
        virtual void get_photo() = 0;
        virtual void send_photo(model::Photo photo) = 0;
    };
}
#endif