mck <- function(ma) {
  tenma <- MCK$MCK
  date_sq <- seq.Date(dmy("20/05/2022"), dmy("25/07/2022"), by = "day")
  
  date_sq <- format(date_sq, "%d/%m/%Y")
  
  df_list <- list()
  #read_excel
  for (i in c(1:length(date_sq))) {
    tryCatch({  
      #webpage <- read_html(paste0(link[i]))
      
      for (j in c(length(tenma))) {
      webpage <- read_html(paste0("https://s.cafef.vn/Lich-su-giao-dich-", tenma[j], "-6.chn?date=", date_sq[i]))
      }
      
      df <- webpage %>%
        html_nodes("table") %>%
        .[2:2] %>%
        html_table(fill = TRUE)
      #str(df)
      
      #df <- df[lapply(df, nrow) > 4] ## Dùng để lọc độ dài quan sát
      
      df <- df[lapply(df, ncol) == 3] ## Dùng để lọc số cột
      df <- do.call(rbind, df)
      #df <- df[,1:4]
      names(df) <- c("Gia", "KL", "tytrong")
      df$KL <- str_remove_all(df$KL, ",")
      df$KL <- as.numeric(df$KL)
      df <- arrange(df, desc(KL))
      df <- df[1:1,]
      
      df$MCK <- tenma[j]
      df$Date <- date_sq[i]
      
      df_list[[i]] <- df
    }, error = function(e) cat("Không có ngày", date_sq[i],"của",tenma[j], '\n'))
  }
  y <- do.call(rbind,df_list)
  rownames(y) <- 1:nrow(y)
  return(y)
}

data <- mck(a) %>% unique()
