#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <mqtt_win.h>


QT_BEGIN_NAMESPACE
namespace Ui {
class Widget;
}
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();

private slots:

    void on_ch_win_state_clicked();

    void on_auto_location_clicked();

    void on_update_data_clicked();
    void update_message();
    void win_state_ch();


private:
    Ui::Widget *ui;

    int win_state = 0;
    mqtt_win *mqtt_w;


};
#endif // WIDGET_H
