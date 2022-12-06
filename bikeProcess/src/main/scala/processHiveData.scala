import com.huaban.analysis.jieba.JiebaSegmenter
import org.apache.hadoop.hdfs.protocol.proto.ClientNamenodeProtocolProtos.SetQuotaRequestProto
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}

import java.util.Properties
import scala.collection.mutable.ArrayBuffer
import scala.util.matching.Regex

object processHiveData {
  val MYSQL_HOST = "test" // mysql所在主机host
  val MYSQL_PORT = 3306 // mysql所在主机的mysql的端口
  val MYSQL_DB = "bike" // 希望存储到的数据库名称
  val MYSQL_USER = "root" // mysql用户
  val MYSQL_PWD = "123456" // mysql密码
  val MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver" // mysql驱动，如果pom中的版本是5.1.x版本,改为com.mysql.jdbc.Driver
  // 查询的数据库和表
  val SELECT_DB = "bike"
  val SELECT_TABLE = "bike"

  def main(args: Array[String]): Unit = {
    val sparkSession = SparkSession.builder().master("local").appName("bike")
      .enableHiveSupport().getOrCreate()

    // selectSimpleTemp(sparkSession,Array("*"),"instant","instant asc").show(5)
    // cnt分区统计
    useRate(sparkSession)
  }

  // 全部放一个函数里
  def oneStep(sparkSession: SparkSession): Unit = {
    // 按季节分组统计
    var dataframe = selectSimpleTemp(sparkSession, Array("season", "sum(cnt) season_cnt"), "season", "season asc")
    dataframe2Mysql(dataframe, "season_sum")
    // 按季节分组均值
    dataframe = selectSimpleTemp(sparkSession, Array("season", "round(avg(cnt),2) season_avg"), "season", "season asc")
    dataframe2Mysql(dataframe, "season_avg")
    // 年份统计
    dataframe = selectSimpleTemp(sparkSession, Array("yr", "sum(cnt) yr_cnt"), "yr", "yr asc")
    dataframe2Mysql(dataframe, "yr_cnt")
    // 月份统计
    dataframe = selectSimpleTemp(sparkSession, Array("mnth", "sum(cnt) mnth_cnt"), "mnth", "mnth asc")
    dataframe2Mysql(dataframe, "mnth_cnt")
    // 月份平均
    dataframe = selectSimpleTemp(sparkSession, Array("mnth", "round(avg(cnt),2) mnth_avg"), "mnth", "mnth asc")
    dataframe2Mysql(dataframe, "mnth_avg")
    // 假期平均
    dataframe = selectSimpleTemp(sparkSession, Array("holiday", "round(avg(cnt),2) holiday_avg"), "holiday", "holiday asc")
    dataframe2Mysql(dataframe, "holiday_avg")
    // 星期平均
    dataframe = selectSimpleTemp(sparkSession, Array("weekday", "round(avg(cnt),2) week_avg"), "weekday", "weekday asc")
    dataframe2Mysql(dataframe, "week_avg")
    // 天气统计
    dataframe = selectSimpleTemp(sparkSession, Array("weathersit", "sum(cnt) weathersit_cnt"), "weathersit", "weathersit asc")
    dataframe2Mysql(dataframe, "weathersit_cnt")
  }

  // 查询模版
  def selectSimpleTemp(sparkSession: SparkSession, fields: Array[String], groupBy: String, orderBy: String): DataFrame = {
    val str_f = fields.mkString(",") // 用逗号拼接
    val db_t = SELECT_DB + "." + SELECT_TABLE
    val dataFrame = sparkSession.sql(f"select " + str_f + " from " + db_t + " group by " + groupBy + " order by " + orderBy)
    dataFrame
  }

  //写入mysql模版
  def dataframe2Mysql(dataframe: DataFrame, tableName: String): Unit = {
    dataframe.write.mode(SaveMode.Overwrite).format("jdbc")
      .option("url", "jdbc:mysql://" + MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_DB + "?createDatabaseIfNotExist=true&useSSL=false&useUnicode=true&characterEncoding=UTF-8")
      .option("driver", "com.mysql.cj.jdbc.Driver")
      .option("dbtable", tableName)
      .option("user", MYSQL_USER)
      .option("password", MYSQL_PWD)
      .save()
  }


  // cnt分区
  def cntSection(sparkSession: SparkSession): Unit = {
    sparkSession.sql("select cnt from " + SELECT_DB+"."+SELECT_TABLE).createOrReplaceTempView("v1")
    sparkSession.sql("select case " +
      "when cnt <= 1000 then '0~1000' " +
      "when cnt <= 2000 then '1000~2000' " +
      "when cnt <= 3000 then '2000~3000' " +
      "when cnt <= 4000 then '3000~4000' " +
      "when cnt <= 5000 then '4000~5000' " +
      "when cnt <= 6000 then '5000~6000' " +
      "else '6000+' end cnt_section from v1").createOrReplaceTempView("v2")
    val dataFrame = sparkSession.sql("select cnt_section,count(cnt_section) from v2 group by cnt_section sort by cnt_section")
    dataFrame.show()
    dataframe2Mysql(dataFrame,"cnt_section")
  }

  // 使用百分比统计
  def useRate(sparkSession: SparkSession): Unit ={
    sparkSession.sql("select round(registered/cnt,4)*100 use_rate from "+SELECT_DB+"."+SELECT_TABLE).createOrReplaceTempView("v1")
    sparkSession.sql("select case " +
      "when use_rate <= 60 then '0~60%' " +
      "when use_rate <= 70 then '60%~70%' " +
      "when use_rate <= 80 then '70%~80%' " +
      "when use_rate <= 90 then '80%~90%' " +
      "else '90%+' end use_rate from v1").createOrReplaceTempView("v2")
    val dataFrame = sparkSession.sql("select use_rate,count(use_rate) from v2 group by use_rate order by use_rate")
    dataFrame.show()
    dataframe2Mysql(dataFrame,"use_rate")
  }
}
