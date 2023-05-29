#ifndef COMMAND_H
#define COMMAND_H

#include <vector>

// 命令接口
template <typename CommandReceiver>
class ICommand
{
public:
    virtual void execute(CommandReceiver &receiver) = 0;
};

// 具体命令类
template <typename CommandReceiver>
class RelayCommand : public ICommand<CommandReceiver>
{
public:
    void execute(CommandReceiver &receiver) override;
};

// 接收者类
class CommandReceiver
{
public:
    void action();
};

// 调用者类
template <typename CommandReceiver>
class CommandInvoker
{
private:
    std::vector<ICommand<CommandReceiver> *> commands;

public:
    void addCommand(ICommand<CommandReceiver> *command);
    void executeCommands(CommandReceiver &receiver);
};

#endif // COMMAND_H
