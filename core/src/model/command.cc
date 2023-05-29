#include <command.h>

// 具体命令类实现
template <typename CommandReceiver>
void RelayCommand<CommandReceiver>::execute(CommandReceiver &receiver)
{
    receiver.action();
}

// 接收者类实现
void CommandReceiver::action()
{
}

// 调用者类实现
template <typename CommandReceiver>
void CommandInvoker<CommandReceiver>::addCommand(ICommand<CommandReceiver> *command)
{
    commands.push_back(command);
}

template <typename CommandReceiver>
void CommandInvoker<CommandReceiver>::executeCommands(CommandReceiver &receiver)
{
    for (auto command : commands)
    {
        command->execute(receiver);
    }
}