#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票预测系统 - 主入口文件

该文件是股票预测系统的主要执行入口，包含关注股票列表，
可以批量执行股票预测并生成报告。
"""

import sys
import os
from datetime import datetime

# 将script目录添加到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'script'))

from stock_predictor import StockPredictor


def main():
    """主函数：执行关注股票的批量预测"""
    
    # 🎯 关注股票列表 - 可以在这里添加你关注的股票
    # 格式：只包含股票代码的列表
    # 不要改动
    watch_list = [
        "002208",
        "002156",
        "603162",
        "002320",
        "603938",
        "600408",
        "002825"
    ]
    
    print("🚀 股票预测系统启动")
    print("=" * 60)
    print(f"📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 关注股票数量: {len(watch_list)}")
    print("=" * 60)
    
    # 创建预测器实例
    predictor = StockPredictor()
    
    # 成功和失败计数
    success_count = 0
    fail_count = 0
    
    # 创建数据获取器实例（用于获取股票名称）
    from stock_data_fetcher_akshare import StockDataFetcher
    data_fetcher = StockDataFetcher()
    
    # 遍历关注列表进行预测
    for stock_code in watch_list:
        # 获取股票名称
        stock_name = data_fetcher.get_stock_name(stock_code)
        if not stock_name:
            stock_name = "未知股票"
        
        print(f"\n📈 正在分析 {stock_code} - {stock_name}")
        print("-" * 40)
        
        try:
            # 执行股票预测（包含新闻分析）
            result = predictor.predict_stock_trend(
                stock_code=stock_code,
                days=30,  # 获取30天历史数据
                include_news=True  # 包含新闻分析
            )
            
            if result['success']:
                # 保存预测报告（使用新的文件名格式）
                report_path = predictor.save_prediction_report(
                    result=result,
                    stock_name=stock_name  # 传入股票名称
                )
                
                print(f"✅ 预测成功！")
                print(f"📄 报告已保存: {report_path}")
                
                # 显示预测结果摘要
                prediction_lines = result['prediction'].split('\n')[:10]
                print(f"\n🔮 预测摘要:")
                for line in prediction_lines:
                    if line.strip():
                        print(f"  {line}")
                
                success_count += 1
                
            else:
                print(f"❌ 预测失败: {result['error']}")
                fail_count += 1
                
        except Exception as e:
            print(f"❌ 分析 {stock_code} 时发生错误: {str(e)}")
            fail_count += 1
        
        # 短暂延迟，避免请求过快
        import time
        time.sleep(1)
    
    # 总结报告
    print("\n" + "=" * 60)
    print("📋 批量预测完成总结")
    print("=" * 60)
    print(f"✅ 成功: {success_count} 只股票")
    print(f"❌ 失败: {fail_count} 只股票")
    print(f"📊 总计: {len(watch_list)} 只股票")
    
    if success_count > 0:
        print(f"\n📁 所有预测报告已保存到: prediction/{datetime.now().strftime('%Y/%m/%d')}/ 目录下")
        print(f"📄 文件名格式: 股票代码_股票名称_年月日.md")
    
    print("\n🎉 批量预测执行完成！")
    
    # 自动执行git push操作
    print("\n📤 正在执行Git推送操作...")
    try:
        import subprocess
        
        # 添加所有预测报告文件
        print("📥 添加预测报告文件...")
        result = subprocess.run(['git', 'add', 'script/prediction/'], 
                              capture_output=True, text=True, cwd='/Users/zhezhang/Documents/A')
        if result.returncode != 0:
            print(f"⚠️ 添加文件时出错: {result.stderr}")
        else:
            print("✅ 文件添加成功")
        
        # 提交更改
        commit_message = f"📊 添加股票预测报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"💾 提交更改: {commit_message}")
        result = subprocess.run(['git', 'commit', '-m', commit_message], 
                              capture_output=True, text=True, cwd='/Users/zhezhang/Documents/A')
        if result.returncode != 0:
            if "nothing to commit" in result.stderr:
                print("ℹ️ 没有新的更改需要提交")
            else:
                print(f"⚠️ 提交时出错: {result.stderr}")
        else:
            print("✅ 提交成功")
        
        # 推送到远程仓库
        print("🚀 推送到远程仓库...")
        result = subprocess.run(['git', 'push'], 
                              capture_output=True, text=True, cwd='/Users/zhezhang/Documents/A')
        if result.returncode != 0:
            print(f"⚠️ 推送时出错: {result.stderr}")
        else:
            print("✅ Git推送成功完成！")
            print("📦 预测报告已上传到远程仓库")
            
    except FileNotFoundError:
        print("⚠️ 未找到Git命令，请确保已安装Git")
    except Exception as e:
        print(f"⚠️ Git操作失败: {str(e)}")
    
    print("\n🎯 所有操作完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断执行")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 系统错误: {str(e)}")
        sys.exit(1)