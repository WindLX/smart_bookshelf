#include <photo.h>
#include <option.h>

model::Photo::Photo()
{
    this->type = utils::Option<PhotoType>();
    this->data = utils::Option<std::vector<unsigned char>>();
}

explicit model::Photo::Photo(PhotoType type)
{
    this->type = utils::Option<PhotoType>(type);
    this->data = utils::Option<std::vector<unsigned char>>();
}

model::Photo::Photo(PhotoType type, const std::vector<unsigned char> &data)
{
    this->type = utils::Option<PhotoType>(type);
    this->data = utils::Option<std::vector<unsigned char>>(data);
}

model::Photo::~Photo() {}

void model::Photo::set_type(PhotoType type)
{
    this->type = utils::Option<PhotoType>(type);
}

utils::Option<model::PhotoType> model::Photo::get_type() const
{
    return this->type;
}

void model::Photo::set_data(const std::vector<unsigned char> &data)
{
    this->data = data;
}

utils::Option<std::vector<unsigned char>> model::Photo::get_data() const
{
    return this->data;
}
