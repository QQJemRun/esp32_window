#include "widget.h"
#include "ui_widget.h"
#include <QGeoCoordinate>
#include <QGeoPositionInfoSource>
#include <QDebug>
#include <QMessageBox>

#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QJsonObject>
#include <QJsonValue>
#include <QUrl>
#include <QNetworkReply>
#include <QJsonDocument>



QString BASE_URL = "https://api.caiyunapp.com/v2.6/fuwhPNzXsYXIvMya/";


Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
    this->setAttribute(Qt::WA_StyledBackground);
    mqtt_w = new mqtt_win;
    this->hide();
    mqtt_w->show();
    connect(mqtt_w,&mqtt_win::started,this,[=]()
            {
        this->show();
        mqtt_w->hide();
    });
    connect(mqtt_w,&mqtt_win::new_message,this,[=](QString msg)
            {
        qDebug()<<msg;
        ui->air_in_the_room->clear();
        ui->air_out_of_the_room->clear();
        QJsonDocument doc = QJsonDocument::fromJson(msg.toLocal8Bit().data());
        QJsonObject air_in = QJsonDocument::fromJson(doc.object()["items"].toObject()["aqi_in_the_room"].toObject()["value"].toString().toLocal8Bit().data()).object();

        for(auto key : air_in.keys())
        {
            if(air_in[key].isDouble())
                ui->air_in_the_room->append(QString("%1").arg(key, 12, QLatin1Char(' '))+'\t'+QString::number(air_in[key].toDouble()));
            else if(air_in[key].isString())
                ui->air_in_the_room->append(QString("%1").arg(key, 12, QLatin1Char(' '))+'\t'+air_in[key].toString());
            else
                ui->air_in_the_room->append(QString("%1").arg(key, 12, QLatin1Char(' '))+'\t'+QString::number(air_in[key].toInt()));
        };

        QJsonObject air_out = QJsonDocument::fromJson(doc.object()["items"].toObject()["aqi_out_of_door"].toObject()["value"].toString().toLocal8Bit().data()).object();

        for(auto key : air_out.keys())
        {
            if(air_out[key].isDouble())
                ui->air_out_of_the_room->append(QString("%1").arg(key, 12, QLatin1Char(' '))+'\t'+QString::number(air_out[key].toDouble()));
            else if(air_out[key].isString())
                ui->air_out_of_the_room->append(QString("%1").arg(key, 12, QLatin1Char(' '))+'\t'+air_out[key].toString());
            else
                ui->air_out_of_the_room->append(QString("%1").arg(key, 12, QLatin1Char(' '))+'\t'+QString::number(air_out[key].toInt()));
        };
        qDebug()<<this->win_state<<"\t"<<doc.object()["items"].toObject()["win_state"].toObject()["value"].toInt();
        if (this->win_state == doc.object()["items"].toObject()["win_state"].toObject()["value"].toInt())
            return;
        else
        {
            // this->win_state = doc.object()["items"].toObject()["win_state"].toObject()["value"].toInt();
            ui->ch_win_state->click();
        }
    });
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_ch_win_state_clicked()
{
    if(this->win_state == 0)
    {
        this->win_state = 1;
        QJsonObject message,params;
        params.insert("aqi_out_of_door", "开窗");
        params.insert("aqi_in_the_room", "开窗");
        params.insert("win_state",1);
        params.insert("temperature",0);
        params.insert("openning_time",-1);
        message.insert("params",params);
        message.insert("version","1.0.0");
        mqtt_w->send_message(QString(QJsonDocument(message).toJson()));

        ui->win_icon->setStyleSheet("image: url(:/win_openning.png);background-color: rgba(87, 227, 137,150);border-radius:20px;");
        ui->ch_win_state->setText("关窗");
    }
    else
    {
        this->win_state = 0;
        QJsonObject message,params;
        params.insert("aqi_out_of_door", "关窗");
        params.insert("aqi_in_the_room", "关窗");
        params.insert("win_state",0);
        params.insert("humidity",0);
        params.insert("temperature",0);
        params.insert("openning_time",-1);
        message.insert("params",params);
        message.insert("version","1.0.0");
        mqtt_w->send_message(QString(QJsonDocument(message).toJson()));
        ui->win_icon->setStyleSheet("image: url(:/win_closing.png);background-color: rgba(98, 160, 234,150);border-radius:20px;");
        ui->ch_win_state->setText("开窗");
    }
}


void Widget::win_state_ch()
{

    return;
}



void Widget::on_auto_location_clicked()
{
    QGeoPositionInfoSource *source = QGeoPositionInfoSource::createDefaultSource(this);
    if (source) {
        connect(source, &QGeoPositionInfoSource::positionUpdated,this,[=](const QGeoPositionInfo &info)
                {
                    qDebug()<<info;
                    ui->longitude->setText(QString::number(info.coordinate().longitude()));
                    ui->latitude->setText(QString::number(info.coordinate().latitude()));
                    source->stopUpdates();
                });
        source->startUpdates();
    }
    else
    {
        qDebug()<<"defeat";
    }
}

void Widget::update_message()
{

}



void Widget::on_update_data_clicked()
{
    QJsonObject message,params;
    params.insert("aqi_out_of_door", "");
    params.insert("aqi_in_the_room", "");
    params.insert("win_state",this->win_state);
    params.insert("humidity",0);
    params.insert("temperature",0);
    params.insert("openning_time",ui->openning_time->value());
    message.insert("params",params);
    message.insert("version","1.0.0");
    mqtt_w->send_message(QString(QJsonDocument(message).toJson()));
}

